from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import CustomUser,Profile
from .forms import CustomUserCreationForm, UserVerificationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = UserVerificationForm
    model = CustomUser
    list_display = ('username', 'email', 'is_verified', 'is_staff')
    list_filter = ('is_verified', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email')}),
        ('دسترسی‌ها', {
            'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('تاریخ‌های مهم', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'job_position')
    readonly_fields = ('display_image',)

    def display_image(self, obj):
        if obj.profile_image:
            return mark_safe(f'<img src="{obj.profile_image.url}" width="100" />')
        return "بدون عکس"

    display_image.short_description = "پیش‌نمایش عکس"
admin.site.register(CustomUser, CustomUserAdmin)