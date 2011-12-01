from notifications.engine import NotificationEngine
from notifications import settings as notification_settings


class BackendError(Exception):
    pass


class NotificationLevelError(Exception):
    pass


class NotificationActionError(Exception):
    pass


class BaseNotification(object):
    subject = None
    text = None
    user = None
    level = 'info'

    allowed_backends = []
    allowed_levels = ['info', 'success', 'error', 'warning']

    _all_backends = NotificationEngine._backends

    def __init__(self, subject=None, text=None, user=None, level=None, **kwargs):
        if level not in self.allowed_levels:
            raise NotificationLevelError('unknown level "%s", must be one of %s' % (level, ', '.join(self.allowed_levels)))

        # By default all registered backends are allowed
        if not self.allowed_backends:
            self.allowed_backends = NotificationEngine._backends.keys()

        self.subject = subject or self.subject
        self.text = text or self.text
        self.user = user or self.user
        self.level = level or self.level
        self.request = kwargs.pop('request', False) # can't be saved to database, so remove from kwargs
        self.kwargs = kwargs

    def do(self, action='add', backend=False):
        """
        Do something with this notification. By default we send it to the backend, which can decide
        if it needs to go to the queue, or if it will be shown directly.
        The "process" action will be used by the cron job, for the queued notifications.
        """

        if action not in ['add', 'process']:
            raise NotificationActionError('unknown action "%s", must be one of "add" or "process"' % action)

        if backend:
            # We are only interested in one specific backend, so override self.allowed_backends.
            # This is used by the cron job, where a notification is queued for a specific backend.
            self.allowed_backends = [backend]

        backends = self._get_backends()
        results = {}

        for backend_name, backend in backends.items():
            if action == 'add':
                results[backend_name] = backend.create()
            elif action == 'process':
                results[backend_name] = backend.process()

        return results

    def get_text(self, backend):
        return self.text

    def get_subject(self, backend):
        return self.subject

    def _get_backends(self):
        """
        Get the correct backend(s) for this notification.
        Only backends that validate (all required settings are available) apply.
        """
        backends = {}
        for backend_name in self.allowed_backends:
            # TODO: find out if this allowed backend is actually turned on by the user
            backend = self._all_backends[backend_name](notification=self)
            if backend.validate():
                backends[backend_name] = backend

        if not backends and not notification_settings.FAIL_SILENT:
            raise BackendError('Could not find a backend for this notification')

        return backends
