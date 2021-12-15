from django.core.mail import send_mail

from staff_app_bkend.celery import app
from staff_app_bkend.settings import EMAIL_HOST_USER
from django.template.loader import get_template

@app.task
def add(x, y):
    return x + y
