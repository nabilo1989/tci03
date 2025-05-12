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





class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    # فیلدهای جدید
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")

    GENDER_CHOICES = [
        ('male', 'مرد'),
        ('female', 'زن'),
    ]
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name="جنسیت"
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        verbose_name="عکس پروفایل"
    )

    JOB_POSITION_CHOICES = [
        ('staff', 'کارمند'),
        ('manager', 'مدیر'),
    ]
    job_position = models.CharField(
        max_length=50,
        choices=JOB_POSITION_CHOICES,
        verbose_name="سمت شغلی"
    )
    position = models.CharField(max_length=100, blank=True, null=True)  # استاد، دانشجو، کارمند و...

    def __str__(self):
        return f"{self.user.username}{self.last_name} - {self.get_job_position_display()}'s Profile"