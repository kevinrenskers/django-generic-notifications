from django.conf import settings
from django.contrib import messages
from notifications.backend import BaseNotificationBackend, MissingRequestError, BackendConfigError
from notifications import settings as notification_settings


class DjangoMessagesNotificationBackend(BaseNotificationBackend):
    """
    A backend that uses Django's messages app to show the notification in the html template.
    See https://docs.djangoproject.com/en/1.3/ref/contrib/messages/
    """
    process_method = 'direct'

    def validate(self):
        """
        This backend can only function when there a request object. This must be supplied to the notification type.
        Also check if the messages app is installed correctly.
        """
        if not self.notification.request:
            if notification_settings.FAIL_SILENT:
                return False
            raise MissingRequestError('DjangoMessagesNotificationBackend needs the request object, you need to pass it to %s()' % self.notification.__class__.__name__)

        if 'django.contrib.messages.middleware.MessageMiddleware' not in settings.MIDDLEWARE_CLASSES:
            if notification_settings.FAIL_SILENT:
                return False
            raise BackendConfigError('You need to add django.contrib.messages.middleware.MessageMiddleware to MIDDLEWARE_CLASSES')

        if 'django.contrib.messages.context_processors.messages' not in settings.TEMPLATE_CONTEXT_PROCESSORS:
            if notification_settings.FAIL_SILENT:
                return False
            raise BackendConfigError('You need to add django.contrib.messages.context_processors.messages to TEMPLATE_CONTEXT_PROCESSORS')

        self.text = self.notification.get_text(self) or self.notification.get_subject(self)

        if not self.text:
            return False

        return True

    def process(self):
        # Translate notification level to django message level
        levels = {
            'info': messages.INFO,
            'success': messages.SUCCESS,
            'error': messages.ERROR,
            'warning': messages.WARNING,
        }

        level = levels.get(self.notification.level, messages.INFO)

        return messages.add_message(self.notification.request, level, self.text)
