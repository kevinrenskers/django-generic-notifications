from django.contrib.auth.models import User
from django.db import models

from notifications.engine import NotificationEngine
from notifications.type.account import AccountNotification
from notifications.type.default import DefaultNotification
from notifications.backend.django_email import DjangoEmailNotificationBackend


class NotificationQueue(models.Model):
    """
    The queue is used for backends that have show_method set to "queue"
    """
    user = models.ForeignKey(User, related_name='notifications')
    subject = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    tries = models.PositiveIntegerField(default=0)
    backend = models.CharField(max_length=40)

    def __unicode__(self):
        return self.text

    def get_backend(self):
        return NotificationEngine._backends[self.backend]


# Register all notification types
NotificationEngine.register_type(DefaultNotification)
NotificationEngine.register_type(AccountNotification)

# Register all default backends
NotificationEngine.register_backend(DjangoEmailNotificationBackend)
