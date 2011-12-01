Usage
=====
Simple example of use cases::

    from notifications.type.default import DefaultNotification
    DefaultNotification('Subject', 'This is a notification!', request=request).do('add')

    from notifications.type.account import AccountNotification
    AccountNotification('Account created', 'Your account has been created!', user=request.user).do('add')
    AccountNotification('Account created', 'Your account has been created!', email='hello@example.com').do('add')


Cron
====
There is a command to process notifications that have been added to the queue::

    ./manage.py process_notifications

You will need to set up a cron job that calls this command periodically.
