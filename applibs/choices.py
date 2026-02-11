from django.db import models

class AuthProvider(models.TextChoices):
    GOOGLE = 'google', 'Google'
    LOCAL = 'local', 'Local'