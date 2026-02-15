import ulid
from typing import Any, Optional

from django.db import models
from django.utils import timezone
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

    def get_user_by_email(self, email: str) -> Optional[AbstractUser]:
        try:
            user = self.get(email=email)
            return user
        except self.model.DoesNotExist:
            return None

    def email_exists(self, email: str) -> bool:
        email = self.normalize_email(email)
        return self.filter(email=email).exists()

class User(AbstractUser):
    id = models.CharField(max_length=26, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=55)
    date_joined = models.DateTimeField(default=timezone.now)
    auth_provider = models.CharField(
        max_length=10,
        choices=AuthProvider.choices,
        default=AuthProvider.EMAIL
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(ulid.new())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'