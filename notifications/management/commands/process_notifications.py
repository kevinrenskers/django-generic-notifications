from django.core.management.base import NoArgsCommand
from django.db.models import F
from notifications.models import NotificationQueue
from notifications import settings as notification_settings


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        notifications = NotificationQueue.objects.all()

        for notification in notifications:
            if notification.tries >= notification_settings.QUEUE_MAX_TRIES:
                # Don't try it any more
                # TODO: logging, email error, etc
                notification.delete()
                continue

            notification_class = notification.get_type()

            result = notification_class(
                subject=notification.subject,
                text=notification.text,
                user=notification.user,
                level=notification.level,
                **notification.extra_context
            ).do('process')

            if result:
                # success, simply delete the notification from the queue
                notification.delete()
            else:
                # error, update the try counter
                # TODO: logging, email error, etc
                notification.tries = F('tries') + 1
                notification.save()
