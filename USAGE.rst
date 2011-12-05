Usage
=====
Simple example of use cases::

    from notifications.type.default import DefaultNotification
    DefaultNotification('Subject', 'This is a notification!', request=request).add()

    from notifications.type.account import AccountNotification
    AccountNotification('Account created', 'Your account has been created!', user=request.user).add()
    AccountNotification('Account created', 'Your account has been created!', email='hello@example.com').add()
