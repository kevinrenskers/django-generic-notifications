from django.conf import settings

QUEUE_MAX_TRIES = getattr(settings, 'NOTIFICATION_QUEUE_MAX_TRIES', 5)
FAIL_SILENT = getattr(settings, 'NOTIFICATION_FAIL_SILENT', True)
