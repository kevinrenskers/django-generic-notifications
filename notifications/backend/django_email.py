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

        self.to = self.user.email
        self.from_address = settings.DEFAULT_FROM_EMAIL

        if not self.to:
            if notification_settings.FAIL_SILENT:
                return False
            raise MissingEmailError('EmailNotificationBackend needs an email address.')

        if not self.from_address:
            if notification_settings.FAIL_SILENT:
                return False
            raise MissingEmailError('EmailNotificationBackend needs a from address.')

        return True

    def process(self):
        """
        Send email using Django's standard email function
        """
        return send_mail(
            self.subject,
            self.text,
            self.from_address,
            self._validate_list(self.to)
        )
