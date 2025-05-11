from django.db import models
from accounts.models import CustomUser
import csv
from io import StringIO
from django.core.exceptions import ValidationError

class Contact(models.Model):
    """
    Model representing a contact in the phonebook.
    """
    first_name = models.CharField(
        max_length=100,
        verbose_name='نام'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='نام خانوادگی'
    )
    landline = models.CharField(
        max_length=15,
        verbose_name='تلفن ثابت',
        blank=True,
        null=True
    )
    office_phone = models.CharField(
        max_length=15,
        verbose_name='تلفن دفتر',
        blank=True,
        null=True
    )
    mobile = models.CharField(
        max_length=15,
        verbose_name='موبایل',
        blank=True,
        null=True
    )
    position = models.CharField(
        max_length=100,
        verbose_name='سمت شغلی',
        blank=True,
        null=True
    )
    workplace = models.CharField(
        max_length=200,
        verbose_name='محل کار',
        blank=True,
        null=True
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='ایجاد شده توسط'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ به‌روزرسانی'
    )

    @classmethod
    def import_from_csv(cls, csv_file, user):
        """
        Import contacts from a CSV file
        """
        try:
            # Read the CSV file
            data = csv_file.read().decode('utf-8-sig')
            reader = csv.DictReader(StringIO(data))

            created_count = 0
            error_messages = []

            for row in reader:
                try:
                    # Create contact from row data
                    contact = cls(
                        first_name=row.get('first_name', row.get('نام', '')),
                        last_name=row.get('last_name', row.get('نام خانوادگی', '')),
                        landline=row.get('landline', row.get('تلفن ثابت', '')),
                        office_phone=row.get('office_phone', row.get('تلفن دفتر', '')),
                        mobile=row.get('mobile', row.get('موبایل', '')),
                        position=row.get('position', row.get('سمت شغلی', '')),
                        workplace=row.get('workplace', row.get('محل کار', '')),
                        created_by=user
                    )
                    contact.full_clean()  # Validate the model
                    contact.save()
                    created_count += 1
                except (ValueError, ValidationError) as e:
                    error_messages.append(f"Error in row {reader.line_num}: {str(e)}")

            return created_count, error_messages

        except Exception as e:
            raise ValueError(f"Error processing CSV file: {str(e)}")
    class Meta:
        verbose_name = 'مخاطب'
        verbose_name_plural = 'مخاطبین'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"