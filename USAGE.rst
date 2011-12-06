Usage
=====
Simple example of use cases::

    from notifications.type.default import DefaultNotification
    DefaultNotification('Subject', 'This is a notification!', request=request).send()

    from notifications.type.account import AccountNotification
    AccountNotification('Account created', 'Your account has been created!', user=request.user).send()

    # Your own subclass, which overrides get_subject, get_text and get_recipients
    NewForumReplyNotification(post=forumpost).send()
