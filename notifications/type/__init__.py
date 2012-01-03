from notifications.engine import NotificationEngine
from notifications import settings as notification_settings


class BackendError(Exception):
    pass

class NotificationTypeError(Exception):
    pass

class BaseNotification(object):
    name = None
    help = ''

    subject = None
    text = None
    send_at = None
    allowed_backends = []

    _all_backends = NotificationEngine._backends

    @classmethod
    def get_name(cls):
        return cls.name or cls.__name__

    @classmethod
    def get_help(cls):
        return cls.help

    def __init__(self, subject=None, text=None, request=None, user=None, **kwargs):
        # By default all registered backends are allowed
        if not self.allowed_backends:
            self.allowed_backends = NotificationEngine._backends.keys()

        self.subject = subject or self.subject
        self.text = text or self.text
        self.user = user
        self.request = request
        self.kwargs = kwargs

    def is_registered(self):
        return self.__class__.__name__ in NotificationEngine._types

    def send(self):
        # Is this type registered? If not, we can't do anything
        if not self.is_registered():
            if notification_settings.FAIL_SILENT:
                return False
            raise NotificationTypeError('No recipients found for this notification')

        users = self.get_recipients()

        # Force users to be a list
        if not hasattr(users, '__iter__'):
            users = [users]

        if not users and not notification_settings.FAIL_SILENT:
            raise NotificationTypeError('No recipients found for this notification')

        for user in users:
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

        return user

    def get_text(self, backend, user):
        return self.text

    def get_subject(self, backend, user):
        return self.subject

    def get_send_at(self, backend, user):
        return self.send_at

    def _get_backends(self, user):
        """
        Get the correct backend(s) for this notification.
        Only backends that validate (all required settings are available) apply.
        """

        from notifications.models import DisabledNotificationsTypeBackend

        disabled_backends = []

        try:
            disabled_backends = DisabledNotificationsTypeBackend.objects.get(user=user, notification_type=self.__class__.__name__).get_backends()
        except DisabledNotificationsTypeBackend.DoesNotExist:
            pass

        backends = {}
        for backend_name in self.allowed_backends:
            if backend_name not in disabled_backends:
                subject = self.get_subject(backend_name, user)
                text = self.get_text(backend_name, user)
                send_at = self.get_send_at(backend_name, user)
                backend = self._all_backends[backend_name](user=user, subject=subject, text=text, send_at=send_at)
                if backend.is_registered() and backend.validate():
                    backends[backend_name] = backend

        if not backends and not notification_settings.FAIL_SILENT:
            raise BackendError('Could not find a backend for this notification')

        return backends

    def __getattr__(self, name):
        # Makes it much easier to access the keyword arguments
        # http://docs.python.org/reference/datamodel.html#customizing-attribute-access
        return self.kwargs[name]
