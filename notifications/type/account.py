from notifications.type import BaseNotification


class AccountNotification(BaseNotification):
    """
    Notifications that deal with your account will only go to the EmailNotificationBackend
    """
    allowed_backends = ['EmailNotificationBackend']
