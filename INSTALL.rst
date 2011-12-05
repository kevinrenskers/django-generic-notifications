Install
=======

1. Get the code: ``pip install django-generic-notifications``
2. Add 'notifications' to your INSTALLED_APPS
3. Add ``url(r'^notifications/settings/$', include('notifications.urls')),`` to urls.py
4. Sync the database (south migrations are provided)
5. Add ``./manage.py process_notifications`` to your cron
