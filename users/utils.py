

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator


def send_email_verify(request, reader):

    current_site = get_current_site(request)
    domain = current_site.domain
    site_name = current_site.name

    context = {
        "domain": domain,
        "site_name": site_name,
        "uid": urlsafe_base64_encode(force_bytes(reader.pk)),
        "reader": reader,
        "token": default_token_generator.make_token(reader),
        "protocol": 'http',
    }

    massage_for_email = render_to_string(
        template_name='users/activate_user_email.html',
        context=context,
        request=request,
    )

    email_message = EmailMultiAlternatives(
        'Подтвержждение учетной записи',
        massage_for_email,
        None,
        [reader.email]
    )

    email_message.send()


def send_email_for_author_application(request, context):

    current_site = get_current_site(request)
    domain = current_site.domain
    context.update({'domain': domain, "protocol": 'http'})

    html_body = render_to_string(
        template_name='users/author_registration_email.html',
        context=context,
        request=request,
    )

    email_message = EmailMultiAlternatives(
        'Заявка на членство в авторах',
        html_body,
        None,
        ['e.aglya@yandex.ru']
    )
    photo = context['photo']

    email_message.attach_alternative(html_body, "text/html")
    email_message.attach(photo.name, photo.read(), photo.content_type)
    email_message.send()
