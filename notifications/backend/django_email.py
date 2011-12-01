from django.conf import settings
from django.core.mail import send_mail
from notifications.backend import BaseNotificationBackend
from notifications import settings as notification_settings


class MissingEmailError(Exception):
    pass


class DjangoEmailNotificationBackend(BaseNotificationBackend):
    """
    A backend that sends email using Django's standard send_mail function.
    """
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

    def validate(self):
        """
        This backend can only function when there are to and from addresses.
        The to address can either be supplied to the notification type, or the logged in user should be supplied.
        The from address can either be supplied, or should be set as settings.DEFAULT_FROM_EMAIL
        """
        to = self.notification.kwargs.get('email', False)
        if not to and hasattr(self.notification.user, 'email'):
            to = self.notification.email

        from_address = self.notification.kwargs.get('from', settings.DEFAULT_FROM_EMAIL)

        if not to:
            if notification_settings.FAIL_SILENT:
                return False
            raise MissingEmailError('EmailNotificationBackend needs an email address. Either set an user or provide %s with an "email" argument.' % self.notification.__class__.__name__)

        if not from_address:
            if notification_settings.FAIL_SILENT:
                return False
            raise MissingEmailError('EmailNotificationBackend needs a from address. Either set settings.DEFAULT_FROM_EMAIL or provide %s with a "from" argument.' % self.notification.__class__.__name__)

        self.to = to
        self.from_address = from_address

        return True

    def process(self):
        """
        Send email using Django's standard email function
        """
        return send_mail(
            self.notification.get_subject(self),
            self.notification.get_text(self),
            self.from_address,
            self._validate_list(self.to)
        )
