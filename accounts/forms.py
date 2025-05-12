from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new users with email and password.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class UserVerificationForm(forms.ModelForm):
    """
    Form for admin to verify users.
    """
    class Meta:
        model = CustomUser
        fields = ('is_verified',)

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'gender',
            'profile_image',
            'job_position',
            'phone',
            'mobile',
        ]
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'gender': 'جنسیت',
            'profile_image': 'عکس پروفایل',
            'job_position': 'سمت شغلی',
            'phone': 'شماره تلفن',
            'mobile': 'موبایل'
        }
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'job_position': forms.Select(attrs={'class': 'form-control'}),
        }