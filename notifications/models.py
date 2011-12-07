from django.contrib.auth.models import User
from django.db import models
from notifications.backend.django_email import DjangoEmailNotificationBackend
from notifications.engine import NotificationEngine

from notifications.fields import JSONField
from notifications.type.account import AccountNotification
from notifications.type.default import DefaultNotification


class NotificationQueue(models.Model):
    """
    The queue is used for backends that have show_method set to "queue"
    """
    user = models.ForeignKey(User, related_name='notifications')
    subject = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    tries = models.PositiveIntegerField(default=0)
    notification_backend = models.CharField(max_length=255)

    def get_backend(self):
        return NotificationEngine._backends[self.notification_backend]

    def __unicode__(self):
        return self.text


class DisabledNotificationsTypeBackend(models.Model):
    """
    In this model we save which backends a user does NOT want to use for a notification type.
    By saving what he does NOT want, new users and new types/backends default to everything.
    """
    user = models.ForeignKey(User)
    notification_type = models.CharField(max_length=255)
    notification_backends = models.TextField()

    def get_backends(self):
        return self.notification_backends.split(',')

    class Meta:
        unique_together = ['user', 'notification_type']


class NotificationBackendSettings(models.Model):
    """
    Model for saving required settings per backend
    """
    user = models.ForeignKey(User)
    notification_backend = models.CharField(max_length=255)
    settings = JSONField()

    class Meta:
        unique_together = ['user', 'notification_backend']


# Register all notification types
NotificationEngine.register_type(DefaultNotification)
NotificationEngine.register_type(AccountNotification)

# Register all default backends
NotificationEngine.register_backend(DjangoEmailNotificationBackend)
