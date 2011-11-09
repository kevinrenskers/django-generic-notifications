from django.conf import settings

QUEUE_MAX_TRIES = getattr(settings, 'NOTIFICATION_QUEUE_MAX_TRIES', 5)
