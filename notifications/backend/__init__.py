class QueueError(Exception):
    pass


class MissingRequestError(Exception):
    pass


class BackendConfigError(Exception):
    pass


class BaseNotificationBackend(object):
    process_method = None

    def __init__(self, notification):
        if self.process_method not in ['queue', 'direct']:
            raise BackendConfigError('You need to set the process_method property of %s to either "queue" or "direct"' % self.__class__.__name__)

        self.notification = notification

    def _queue(self):
        """
        This will add the notification to the database queue. A cron job will then get the notification,
        and call the process() method of its backend.
        """
        from notifications.models import NotificationQueue

        if not self.notification.user and not self.notification.kwargs:
            # If the user is not logged in, then we have no way of getting to his
            # settings, thus unable to email/sms/whatever him.
            # A way around this is to provide kwargs, so his email/phone number/whatever
            # can still be used.
            raise QueueError('Notifications can only be queued for logged in users, or you need to provide kwargs')

        NotificationQueue.objects.create(
            user=self.notification.user,
            subject=self.notification.subject,
            text=self.notification.text,
            level=self.notification.level,
            extra_context=self.notification.kwargs,
            type=self.notification.__class__.__name__
        )

    def _direct(self):
        """
        This will show the notification directly. This is a blocking operation, so should not be
        used for things that take time, like sending email, sms or iPhone push notifications.
        It's useful for Django's messages app, popups, etc.
        """
        return self.process()

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
