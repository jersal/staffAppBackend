from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.template.loader import render_to_string
from staff_app_bkend.settings import EMAIL_HOST_USER


def new_subscription_plaintext_mail(to_user_email):
    subject = 'Welcome to STAFF_APP'
    message = 'Hope you are enjoying the staff_app experience'
    recepient = "ashwinsaji13@gmail.com"
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)


def new_subscription_with_template(to_user_email, *args, **kwargs):
    request_headers = kwargs['request_headers']

    plaintext = get_template('mail_template.txt')
    htmly = get_template('new_mail_template.html')

    # d = Context({'username': to_user_email.name})
    request_origin = request_headers.get('HTTP_ORIGIN', 'http://139.59.70.174:8005').strip()
    d = {'username': to_user_email.name, 'forward_url': '{}/login'.format(request_origin)}

    subject, from_email, to = 'hello', EMAIL_HOST_USER, 'ashwinsaji13@gmail.com'
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

