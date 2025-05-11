from django.contrib import admin
from django.core.exceptions import ValidationError
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
import csv
from io import StringIO
from .models import Contact
from .forms import CSVImportForm


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contact model with CSV import/export functionality.
    """
    list_display = (
        'first_name',
        'last_name',
        'mobile',
        'position',
        'workplace',
        'created_by',
        'created_at'
    )
    list_filter = ('position', 'workplace', 'created_at')
    search_fields = (
        'first_name',
        'last_name',
        'mobile',
        'landline',
        'office_phone',
        'position',
        'workplace'
    )
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    list_per_page = 50
    date_hierarchy = 'created_at'

    # Custom admin templates
    change_list_template = 'admin/contacts/change_list.html'

    fieldsets = (
        (_('اطلاعات اصلی'), {
            'fields': (
                'first_name',
                'last_name',
                'mobile',
                'landline',
                'office_phone'
            )
        }),
        (_('اطلاعات شغلی'), {
            'fields': (
                'position',
                'workplace'
            )
        }),
        (_('اطلاعات سیستمی'), {
            'fields': (
                'created_by',
                'created_at',
                'updated_at'
            )
        }),
    )

    def get_urls(self):
        """
        Add custom URLs for CSV import
        """
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='contacts_contact_import_csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        """
        Handle CSV file imports in admin interface
        """
        if request.method == "POST":
            form = CSVImportForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    csv_file = form.cleaned_data['csv_file']
                    decoded_file = csv_file.read().decode('utf-8-sig')
                    reader = csv.DictReader(StringIO(decoded_file))

                    created_count = 0
                    error_messages = []

                    for row in reader:
                        try:
                            contact = Contact(
                                first_name=row.get('first_name', row.get('نام', '')).strip(),
                                last_name=row.get('last_name', row.get('نام خانوادگی', '')).strip(),
                                landline=row.get('landline', row.get('تلفن ثابت', '')).strip() or None,
                                office_phone=row.get('office_phone', row.get('تلفن دفتر', '')).strip() or None,
                                mobile=row.get('mobile', row.get('موبایل', '')).strip() or None,
                                position=row.get('position', row.get('سمت شغلی', '')).strip() or None,
                                workplace=row.get('workplace', row.get('محل کار', '')).strip() or None,
                                created_by=request.user
                            )
                            contact.full_clean()
                            contact.save()
                            created_count += 1
                        except (ValueError, ValidationError) as e:
                            error_messages.append(
                                _('خطا در ردیف %(line_num)d: %(error)s') % {
                                    'line_num': reader.line_num,
                                    'error': str(e)
                                }
                            )

                    if created_count > 0:
                        self.message_user(
                            request,
                            _('%(count)d مخاطب با موفقیت وارد شدند.') % {'count': created_count},
                            messages.SUCCESS
                        )

                    for error in error_messages:
                        self.message_user(request, error, messages.WARNING)

                    return redirect("..")

                except Exception as e:
                    self.message_user(
                        request,
                        _('خطا در پردازش فایل CSV: %(error)s') % {'error': str(e)},
                        messages.ERROR
                    )
        else:
            form = CSVImportForm()

        context = {
            'form': form,
            'opts': self.model._meta,
            'has_view_permission': self.has_view_permission(request),
            'title': _('وارد کردن مخاطبین از CSV'),
        }
        return render(request, "admin/contacts/import_csv.html", context)

    def changelist_view(self, request, extra_context=None):
        """
        Handle CSV export and custom list view
        """
        if 'export' in request.GET:
            return self.export_csv(request)

        return super().changelist_view(request, extra_context=extra_context)

    def export_csv(self, request):
        """
        Export contacts to CSV file
        """
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="contacts_export.csv"'

        writer = csv.writer(response)

        # Write header row
        writer.writerow([
            _('نام'),
            _('نام خانوادگی'),
            _('تلفن ثابت'),
            _('تلفن دفتر'),
            _('موبایل'),
            _('سمت شغلی'),
            _('محل کار')
        ])

        # Write data rows
        for contact in Contact.objects.all():
            writer.writerow([
                contact.first_name,
                contact.last_name,
                contact.landline or '',
                contact.office_phone or '',
                contact.mobile or '',
                contact.position or '',
                contact.workplace or '',
            ])

        return response

    def save_model(self, request, obj, form, change):
        """
        Set the created_by user when creating a new contact
        """
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        Filter contacts for non-superusers to only show their own contacts
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def has_change_permission(self, request, obj=None):
        """
        Only allow changes to contacts created by the user (unless superuser)
        """
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        return obj.created_by == request.user

    def has_delete_permission(self, request, obj=None):
        """
        Only allow deletion of contacts created by the user (unless superuser)
        """
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        return obj.created_by == request.user