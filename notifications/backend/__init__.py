from notifications.engine import NotificationEngine


class BackendConfigError(Exception):
    pass


class BaseNotificationBackend(object):
    process_method = None
    name = None

    @classmethod
    def get_name(cls):
        return cls.name or cls.__name__

    def __init__(self, user=None, subject=None, text=None, send_at=None):
        if self.process_method not in ['queue', 'direct']:
            raise BackendConfigError('You need to set the process_method property of %s to either "queue" or "direct"' % self.__class__.__name__)

        self.user = user
        self.subject = subject
        self.text = text
        self.send_at = send_at

    def is_registered(self):
        return self.__class__.__name__ in NotificationEngine._backends

    def _queue(self):
        """
        This will add the notification to the database queue. A cron job will then get the notification,
        and call the process() method of its backend.
        """
        from notifications.models import NotificationQueue

        NotificationQueue.objects.create(
            user=self.user,
            subject=self.subject,
            text=self.text,
            send_at=self.send_at,
            notification_backend=self.__class__.__name__
        )

    def _direct(self):
        """
        This will show the notification directly. This is a blocking operation, so should not be
        used for things that take time, like sending email, sms or iPhone push notifications.
        It's useful for Django's messages app, popups, etc.
        """
        return self.process()

    def validate(self):
        """
        Check for required settings. For example, if your backend needs a phone number, check for it here.
        """
        return True

    def create(self):
        """
        Will figure out if this notification should go to the queue,
        or if it should be shown directly.
        """
        if self.process_method == 'queue':
            return self._queue()

        if self.process_method == 'direct':
            return self._direct()

    def process(self):
        """
        This will do the actual processing of the notification.
        Each backend should do it own thing here!
        Should return a boolean, stating if processing the notification was successful.
        """
        raise NotImplementedError('The process method needs to be overridden per notification backend')
