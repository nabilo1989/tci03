from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    is_verified = models.BooleanField(
        default=False,
        verbose_name='تایید شده',
        help_text='تعیین می‌کند که آیا کاربر توسط ادمین تایید شده است یا خیر'
    )

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.username