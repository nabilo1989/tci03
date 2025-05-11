from django import forms
from .models import Contact
import csv
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    """
    Form for creating and updating contacts.
    """
    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at']

class ContactSearchForm(forms.Form):
    """
    Form for searching contacts.
    """
    search_query = forms.CharField(
        required=False,
        label='جستجو',
        widget=forms.TextInput(attrs={'placeholder': 'جستجو...'})
    )

class CSVImportForm(forms.Form):
    """
    Form for importing contacts from CSV file.
    """
    csv_file = forms.FileField(label='فایل CSV')

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        if not csv_file.name.endswith('.csv'):
            raise ValidationError('لطفاً یک فایل CSV انتخاب کنید.')
        return csv_file

class VCFImportForm(forms.Form):
    """
    Form for importing contacts from VCF file.
    """
    vcf_file = forms.FileField(label='فایل VCF')

    def clean_vcf_file(self):
        vcf_file = self.cleaned_data['vcf_file']
        if not vcf_file.name.endswith('.vcf'):
            raise ValidationError('لطفاً یک فایل VCF انتخاب کنید.')
        return vcf_file