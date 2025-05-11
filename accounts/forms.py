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