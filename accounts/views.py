from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

def register(request):
    """
    View for user registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                'ثبت‌نام شما با موفقیت انجام شد. پس از تایید توسط ادمین می‌توانید وارد شوید.'
            )
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """
    View for user profile.
    """
    return render(request, 'accounts/profile.html')

# در فایل views.py


def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    # اگر GET بود، یک فرم نمایش دهید
    return render(request, 'accounts/logout_confirmation.html')

@login_required
def profile(request):
    try:
        profile_instance = request.user.profile
    except:
        profile_instance = None

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,  # برای آپلود عکس
            instance=profile_instance
        )
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile_instance)

    return render(request, 'accounts/profile.html', {'form': form})