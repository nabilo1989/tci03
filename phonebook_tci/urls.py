from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import custom_logout
from contacts import views as contacts_views
from accounts import views as accounts_views
from contacts.views import contact_import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', contacts_views.home, name='home'),
    
    # Authentication URLs
    path('register/', accounts_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', accounts_views.profile, name='profile'),
# URLهای بازیابی رمز عبور
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             success_url=reverse_lazy('password_reset_done')
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    # Contacts URLs
    path('contact/create/', contacts_views.contact_create, name='contact_create'),
    path('contact/<int:pk>/update/', contacts_views.contact_update, name='contact_update'),
    path('contact/<int:pk>/delete/', contacts_views.contact_delete, name='contact_delete'),
    
    # Import/Export URLs
    path('contacts/export/csv/', contacts_views.export_contacts_csv, name='export_contacts_csv'),
    path('contacts/import/csv/', contacts_views.import_contacts_csv, name='import_contacts_csv'),
    path('contact-import/', contact_import, name='contact_import'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)