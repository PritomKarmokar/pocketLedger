from django.db import models
from django.utils.translation import gettext_lazy as _

class AuthProvider(models.TextChoices):
    EMAIL = 'email', _('Email')
    GOOGLE = 'google', _('Google')