from django.contrib.auth.models import User
from django.db import models
from notifications import NotificationEngine
from notifications.fields import JSONField

from notifications.type.account import AccountNotification
from notifications.type.default import DefaultNotification

from notifications.backend.django_messages import DjangoMessagesNotificationBackend
from notifications.backend.email import EmailNotificationBackend


class NotificationQueue(models.Model):
    """
    The queue is used for backends that have show_method set to "queue"
    """
    user = models.ForeignKey(User, blank=True, null=True, related_name='notifications')
    subject = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    level = models.CharField(max_length=40)
    extra_context = JSONField()
    tries = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=40)

    def __unicode__(self):
        return self.text

    def get_type(self):
        return NotificationEngine._types[self.type]


# Register all notification types
NotificationEngine.register_type(DefaultNotification)
NotificationEngine.register_type(AccountNotification)

# Register all backends
NotificationEngine.register_backend(EmailNotificationBackend)
NotificationEngine.register_backend(DjangoMessagesNotificationBackend)
