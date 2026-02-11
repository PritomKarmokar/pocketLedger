import ulid
from typing import Any, Optional

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from applibs.logger import get_logger
from applibs.choices import AuthProvider

logger = get_logger(__name__)

class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> AbstractUser:
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields: Any
    ) -> AbstractUser:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.CharField(max_length=26, primary_key=True, editable=False, unique=True)
    email = models.EmailField(unique=True)
    auth_provider = models.CharField(max_length=10, choices=AuthProvider.choices, default=AuthProvider.LOCAL)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(ulid.new())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        db_table = "users"

    @property
    def profile_response_data(self):
        return {
            "username": self.username,
            "joining_data": self.date_joined.strftime("%d-%m-%Y %H:%M:%S")
        }