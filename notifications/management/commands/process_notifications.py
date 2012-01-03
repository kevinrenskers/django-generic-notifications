from datetime import datetime

from django.core.management.base import NoArgsCommand
from django.db.models import F

from notifications.models import NotificationQueue
from notifications import settings as notification_settings


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        notifications = NotificationQueue.objects.exclude(send_at__gte=datetime.now())

        for notification in notifications:
            if notification.tries >= notification_settings.QUEUE_MAX_TRIES:
                # Don't try it any more
                # TODO: logging, email error, etc
                notification.delete()
                continue

            backend_class = notification.get_backend()
            backend = backend_class(user=notification.user, subject=notification.subject, text=notification.text)

            result = backend.validate()
            if result:
                result = backend.process()

            if result:
                # success, simply delete the notification from the queue
                notification.delete()
            else:
                # error, update the try counter
                # TODO: logging, email error, etc
                notification.tries = F('tries') + 1
                notification.save()
