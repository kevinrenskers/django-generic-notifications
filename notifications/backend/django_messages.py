from django.conf import settings
from django.contrib import messages
from notifications.backend import BaseNotificationBackend, MissingRequestError, BackendConfigError

class DjangoMessagesNotificationBackend(BaseNotificationBackend):
    process_method = 'direct'

    def process(self):
        """
        Creates a message in Django's messages app.
        Also does some sanity checks to see if the messages app was installed correctly.
        """
        if not self.notification.request:
            raise MissingRequestError('DjangoMessagesNotificationBackend needs the request object, you need to pass it to %s()' % self.notification.__class__.__name__)

        if 'django.contrib.messages.middleware.MessageMiddleware' not in settings.MIDDLEWARE_CLASSES:
            raise BackendConfigError('You need to add django.contrib.messages.middleware.MessageMiddleware to MIDDLEWARE_CLASSES')

        if 'django.contrib.messages.context_processors.messages' not in settings.TEMPLATE_CONTEXT_PROCESSORS:
            raise BackendConfigError('You need to add django.contrib.messages.context_processors.messages to TEMPLATE_CONTEXT_PROCESSORS')

        # Translate notification level to django message level
        levels = {
            'info': messages.INFO,
            'success': messages.SUCCESS,
            'error': messages.ERROR,
            'warning': messages.WARNING,
        }

        return messages.add_message(self.notification.request, levels[self.notification.level], self.notification.text)
