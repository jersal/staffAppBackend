from django.core.mail import send_mail

from staff_app_bkend.celery import app
from staff_app_bkend.settings import EMAIL_HOST_USER


@app.task
def new_subscription_create_mail(to_user_email):
    subject = 'Welcome to STAFF_APP'
    message = 'Hope you are enjoying the staff_app experience'
    recepient = "ashwinsaji13@gmail.com"
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)

