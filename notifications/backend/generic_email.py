from notifications.backend.django_email import DjangoEmailNotificationBackend
from generic_email import Email


class GenericEmailNotificationBackend(DjangoEmailNotificationBackend):
    """
    A backend that sends email using https://github.com/kevinrenskers/django-generic-mail.
    It's not registered by default, you will need to do this yourself.
    """
    def process(self):
        text_body = self.notification.kwargs.get('text_body', self.notification.text)
        html_body = self.notification.kwargs.get('html_body', None)
        text_template = self.notification.kwargs.get('text_template', None)
        html_template = self.notification.kwargs.get('html_template', None)

        email = Email(
            to=self.to,
            subject=self.notification.subject,
            text_body=text_body,
            html_body=html_body,
            text_template=text_template,
            html_template=html_template,
            from_address=self.from_address
        )

        return email.send()
