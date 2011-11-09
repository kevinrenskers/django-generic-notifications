from notifications import NotificationEngine


class BackendError(Exception):
    pass


class NotificationLevelError(Exception):
    pass


class NotificationActionError(Exception):
    pass


class BaseNotification(object):
    allowed_backends = NotificationEngine._backends
    allowed_levels = ['info', 'success', 'error', 'warning']

    _all_backends = NotificationEngine._backends

    def __init__(self, subject, text, user=None, level='info', **kwargs):
        if level not in self.allowed_levels:
            raise NotificationLevelError('unknown level "%s", must be one of %s' % (level, ', '.join(self.allowed_levels)))

        self.subject = subject
        self.text = text
        self.user = user
        self.level = level
        self.request = kwargs.pop('request', False) # can't be saved to database, so remove from kwargs
        self.kwargs = kwargs

    def do(self, action='add'):
        """
        Do something with this notification. By default we send it to the backend, which can decide
        if it needs to go to the queue, or if it will be shown directly.
        The "process" action will be used by the cron job, for the queued notifications.
        """
        backend = self._get_backend()
        if action == 'add':
            return backend.create()
        elif action == 'process':
            return backend.process()
        else:
            raise NotificationActionError('unknown action "%s", must be one of "add" or "process"' % action)

    def _find_backend(self):
        """
        Use system settings, user settings and self.allowed_backends
        to find the best backend for showing this notification
        """

        # TODO!!!
        return self.allowed_backends['EmailNotificationBackend']

    def _get_backend(self):
        """
        Get the correct backend and send this notification to it.
        The backend will figure out if the notification should be queued or shown directly.
        """
        backend = self._find_backend()
        if not backend:
            raise BackendError('Could not find a backend for this notification')

        return backend(notification=self)
