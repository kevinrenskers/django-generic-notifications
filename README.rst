========
Overview
========

**A Django app that can handle multiple ways of showing different notification types. It's all based on multiple input
types and output backends.**


Notifications
=============
A notification could be anything:

- there was an error in your form submission
- your account has been created
- your account has been activated
- you have received a private message on a forum
- there is a new comment on your blog
- someone liked your profile
- a message from the administrator

As far as this project is concerned, a notification is nothing more but an (optional) subject, text body, and a level
(info, success, error, warning).

Backends
========
There are multiple output backends. Some possible examples are:

- email
- a popup in your webbrowser
- sms message
- iPhone push notification
- Django's messages app

Some backends can process notifications in real time (Django's messages app for example), and others should run in the
background (sending email, sending push messages to iPhones). Each backend specifies what its mode of operation is.

Notification types
==================
A notification type is the glue between a message (input) and one or more possible backends (output). For example, you
might want to send all account related messages to email only, but notifications about new private messages could go to
email, iPhone push messages, Django's own messages app, you name it.

Each notification type can specify its allowed backend, and each user can specify his preferred output backend(s).
Each notification will then figure out what backend to use based on this information.

Settings
========
Some backends will need extra information from the user, for example a phone number, email address or iPhone device id.

This project doesn't provide a settings app where users can configure these. Instead, this is left to an exercise to the
reader (at least for now). Each output backend can accept a variable number of keyword arguments, so building a custom
backend that needs a new setting isn't a problem.

Queue
=====
Some notification backends can't process in real time, instead adding them to a queue. At this moment, this is based on
a simple database model and a manage.py script which can be used from your cron.

In the future celery tasks should be added too.

Installation
============
See `INSTALL.rst`

Usage
=====
See `USAGE.rst` for examples
