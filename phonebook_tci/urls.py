from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from accounts.views import custom_logout
from contacts import views as contacts_views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', contacts_views.home, name='home'),
    
    # Authentication URLs
    path('register/', accounts_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', accounts_views.profile, name='profile'),
    
    # Contacts URLs
    path('contact/create/', contacts_views.contact_create, name='contact_create'),
    path('contact/<int:pk>/update/', contacts_views.contact_update, name='contact_update'),
    path('contact/<int:pk>/delete/', contacts_views.contact_delete, name='contact_delete'),
    
    # Import/Export URLs
    path('contacts/export/csv/', contacts_views.export_contacts_csv, name='export_contacts_csv'),
    path('contacts/import/csv/', contacts_views.import_contacts_csv, name='import_contacts_csv'),
]