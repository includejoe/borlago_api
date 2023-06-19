from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings


def send_reset_password_email(email_address, reset_code):
    email_subject = "Reset Password"
    context = {"code": reset_code}

    html_content = render_to_string("reset_password_email.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        email_subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [email_address],
    )

    email.attach_alternative(html_content, "text/html")
    return email.send(fail_silently=False)
