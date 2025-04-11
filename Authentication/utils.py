from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import threading


class SendMailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(recipient_email, activation_url):
    subject = 'activate your account on ' + settings.SITE_NAME
    from_email = 'Gauley@demomailtrap.com'
    to_email = [recipient_email]

    html_content = render_to_string('Authentication/activation_email.html', {
                                    'activation_url': activation_url})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, 'text/html')
    SendMailThread(email).start()
    # print(activation_url)


def send_reset_password_email(recipient_email, reset_url):
    subject = 'Reset Your Password on ' + settings.SITE_NAME
    from_email = 'Gauley@demomailtrap.com'
    to_email = [recipient_email]

    html_content = render_to_string('Authentication/reset_password_email.html', {
                                    'reset_url': reset_url})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, 'text/html')
    SendMailThread(email).start()
    # print(reset_url)
