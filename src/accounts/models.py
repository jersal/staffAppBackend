from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

from src.accounts.managers import AuthUserManager


class AuthUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, unique=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into admin site'))

    objects = AuthUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


@receiver(post_save, sender=AuthUser)
def obtain_auth_token(sender, instance=None, created=False, **kwargs):
    """
    An auth token for each user is automatically created when AuthUser model is saved.
    """
    if created and instance:
        token, created = Token.objects.get_or_create(user=instance)
        return token




