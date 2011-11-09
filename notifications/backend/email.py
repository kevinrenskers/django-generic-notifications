from django.conf import settings
from django.core.mail import send_mail
from notifications.backend import BaseNotificationBackend


class MissingEmailError(Exception):
    pass


class EmailNotificationBackend(BaseNotificationBackend):
    process_method = 'queue'

    def _validate_list(self, lst):
        """
        Make sure we end up with a list
        """
        if not lst:
            return []
        if isinstance(lst, basestring):
             return [lst]
        return list(lst)

    def process(self):
        """
        Send email using Django's standard email function
        """
        to = self.notification.kwargs.get('email', False)
        if not to and hasattr(self.notification.user, 'email'):
            to = self.notification.email

        from_address = self.notification.kwargs.get('from', settings.DEFAULT_FROM_EMAIL)

        if not to:
            if settings.DEBUG:
                raise MissingEmailError('EmailNotificationBackend needs an email address. Either set an user or provide %s with an "email" argument.' % self.notification.__class__.__name__)
            return False

        if not from_address:
            if settings.DEBUG:
                raise MissingEmailError('EmailNotificationBackend needs a from address. Either set settings.DEFAULT_FROM_EMAIL or provide %s with a "from" argument.' % self.notification.__class__.__name__)
            return False

        return send_mail(self.notification.subject, self.notification.text, from_address, self._validate_list(to))
