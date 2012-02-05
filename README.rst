========
Overview
========

**A Django app that can handle multiple ways of showing different notification types. It's all based on multiple input
types and output backends.**


Notifications
=============
A notification could be anything:

- you have received a private message on a forum
- there is a new comment on your blog
- someone liked your profile or article
- a new post was created in a thread you follow
- someone answered your poll
- you have a new friend request or follower

As far as this project is concerned, a notification is nothing more but an (optional) subject, text body, and a list of
receivers.

Backends
========
There are multiple output backends. Some possible examples are:

- email
- sms message
- iPhone push notification
- notification center

At this moment only two email backends are provided.

Notification types
==================
A notification type is the glue between a message (input) and one or more possible backends (output). For example, you
might want to send all account related messages to email only, but notifications about new private messages could go to
email, iPhone push messages, Django's own messages app, you name it.

Each notification type can specify its allowed backend(s), and each user can specify his preferred output backend(s).
Each notification will then figure out what backend to use based on this information.

Settings
========
Some backends will need extra information from the user, for example a phone number or email address.

Users can also select which notification types they're interested in, and what possible backends they would like to
receive the message on.

Queue
=====
Most notification backends can't process in real time, instead adding them to a queue. At this moment, this is based on
a simple database model and a manage.py script which can be used from your cron.

In the future celery tasks should be added too.

Installation
============
See `INSTALL.rst`

Usage
=====
See `USAGE.rst` for examples
