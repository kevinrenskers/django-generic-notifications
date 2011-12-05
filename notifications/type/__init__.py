from notifications.engine import NotificationEngine
from notifications import settings as notification_settings


class BackendError(Exception):
    pass


class BaseNotification(object):
    subject = None
    text = None
    allowed_backends = []

    _all_backends = NotificationEngine._backends

    def __init__(self, subject=None, text=None, request=None, user=None, **kwargs):
        # By default all registered backends are allowed
        if not self.allowed_backends:
            self.allowed_backends = NotificationEngine._backends.keys()

        self.subject = subject or self.subject
        self.text = text or self.text
        self.user = user
        self.request = request
        self.kwargs = kwargs

        users = self.get_recipients()
        if not users and not notification_settings.FAIL_SILENT:
            raise BackendError('No recipients found for this notification')

        for user in self.get_recipients():
            backends = self._get_backends(user)
            for backend_name, backend in backends.items():
                # the backend will figure out if it needs to queue or not
                backend.create()

    def get_recipients(self):
        user = self.user

        if not user:
            try:
                user = self.request.user
            except KeyError:
                if notification_settings.FAIL_SILENT:
                    return False
                raise BackendError('No user or request object given. Please give at least one of them, or override get_recipients')

        return [user]

    def get_text(self, backend):
        return self.text

    def get_subject(self, backend):
        return self.subject

    def _get_backends(self, user):
        """
        Get the correct backend(s) for this notification.
        Only backends that validate (all required settings are available) apply.
        """
        backends = {}
        for backend_name in self.allowed_backends:
            # TODO: find out if this allowed backend is actually turned on by the user
            subject = self.get_subject(backend_name)
            text = self.get_text(backend_name)
            backend = self._all_backends[backend_name](user=user, subject=subject, text=text)
            if backend.validate():
                backends[backend_name] = backend

        if not backends and not notification_settings.FAIL_SILENT:
            raise BackendError('Could not find a backend for this notification')

        return backends
