

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


def send_feedback_email(request, context):
    html_body = render_to_string(
        template_name='news/feedback_email.html',
        context=context,
        request=request,
    )
    email_message = EmailMultiAlternatives(
        'Обратная связь',
        html_body,
        None,
        ['e.aglya@yandex.ru']
    )
    email_message.send()
