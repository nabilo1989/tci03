from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
import csv
from .models import Contact
from .forms import ContactForm, ContactSearchForm, CSVImportForm, VCFImportForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    """
    Home view displaying all contacts with search functionality.
    """
    contacts = Contact.objects.all()
    search_form = ContactSearchForm(request.GET or None)

    if search_form.is_valid() and search_form.cleaned_data['search_query']:
        query = search_form.cleaned_data['search_query']
        contacts = contacts.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(landline__icontains=query) |
            Q(office_phone__icontains=query) |
            Q(mobile__icontains=query) |
            Q(position__icontains=query) |
            Q(workplace__icontains=query)
        )

    context = {
        'contacts': contacts,
        'search_form': search_form,
    }
    return render(request, 'contacts/home.html', context)


@login_required
def contact_create(request):
    """
    View for creating a new contact (only for verified users).
    """
    if not request.user.is_verified:
        messages.error(request, 'شما مجوز ایجاد مخاطب جدید را ندارید.')
        return redirect('home')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.created_by = request.user
            contact.save()
            messages.success(request, 'مخاطب با موفقیت ایجاد شد.')
            return redirect('home')
    else:
        form = ContactForm()

    return render(request, 'contacts/contact_form.html', {'form': form})


@login_required
def contact_update(request, pk):
    """
    View for updating an existing contact (only for verified users).
    """
    if not request.user.is_verified:
        messages.error(request, 'شما مجوز ویرایش مخاطب را ندارید.')
        return redirect('home')

    contact = get_object_or_404(Contact, pk=pk)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'مخاطب با موفقیت به‌روزرسانی شد.')
            return redirect('home')
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contacts/contact_form.html', {'form': form})


@login_required
def contact_delete(request, pk):
    """
    View for deleting a contact (only for verified users).
    """
    if not request.user.is_verified:
        messages.error(request, 'شما مجوز حذف مخاطب را ندارید.')
        return redirect('home')

    contact = get_object_or_404(Contact, pk=pk)

    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'مخاطب با موفقیت حذف شد.')
        return redirect('home')

    return render(request, 'contacts/contact_confirm_delete.html', {'contact': contact})


@login_required
def export_contacts_csv(request):
    """
    View for exporting contacts to CSV (admin only).
    """
    if not request.user.is_superuser:
        messages.error(request, 'شما مجوز انجام این عمل را ندارید.')
        return redirect('home')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'نام', 'نام خانوادگی', 'تلفن ثابت', 'تلفن دفتر',
        'موبایل', 'سمت شغلی', 'محل کار'
    ])

    contacts = Contact.objects.all().values_list(
        'first_name', 'last_name', 'landline', 'office_phone',
        'mobile', 'position', 'workplace'
    )

    for contact in contacts:
        writer.writerow(contact)

    return response


@login_required
def import_contacts_csv(request):
    """
    View for importing contacts from CSV (admin only).
    """
    if not request.user.is_superuser:
        messages.error(request, 'شما مجوز انجام این عمل را ندارید.')
        return redirect('home')

    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                Contact.objects.create(
                    first_name=row.get('نام', ''),
                    last_name=row.get('نام خانوادگی', ''),
                    landline=row.get('تلفن ثابت', ''),
                    office_phone=row.get('تلفن دفتر', ''),
                    mobile=row.get('موبایل', ''),
                    position=row.get('سمت شغلی', ''),
                    workplace=row.get('محل کار', ''),
                    created_by=request.user
                )

            messages.success(request, 'مخاطبین با موفقیت از فایل CSV وارد شدند.')
            return redirect('home')
    else:
        form = CSVImportForm()

    return render(request, 'contacts/import_csv.html', {'form': form})


class CSVImportView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'contacts/import_csv.html'
    form_class = CSVImportForm
    success_url = reverse_lazy('home')

    def test_func(self):
        """Only allow verified users or superusers"""
        return self.request.user.is_verified or self.request.user.is_superuser

    def form_valid(self, form):
        csv_file = form.cleaned_data['csv_file']
        try:
            created_count, errors = Contact.import_from_csv(csv_file, self.request.user)

            if created_count > 0:
                messages.success(
                    self.request,
                    f'Successfully imported {created_count} contacts.'
                )

            if errors:
                for error in errors:
                    messages.warning(self.request, error)

        except ValueError as e:
            messages.error(self.request, str(e))

        return super().form_valid(form)