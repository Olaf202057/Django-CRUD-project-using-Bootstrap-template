from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"


def send_multipart_email(template_name, context, subject, to, bcc=None):
    """
    Send a multipart text/html email.

    :param template_name: The path to the template (no extension), assuming both a .txt and .html version are present
    :param context: A dictionary of context elements to pass to the email templates
    :param subject: The subject of the email
    :param to: A list of email addresses to which to send
    :param bcc: A list of email addresses to which to BCC
    :return:
    """
    plaintext = get_template('{}.txt'.format(template_name))
    html = get_template('{}.html'.format(template_name))
    text_content = plaintext.render(context)
    html_content = html.render(context)

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, to, bcc)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
