from django import forms
from datetime import date, timedelta
from .models import Booking
from .models import Contact
from django import forms
from .models import Booking
from datetime import date, timedelta

class BookingForm(forms.ModelForm):
    PACKAGE_CHOICES = [
        ('basic', 'Basic Fun ($199)'),
        ('premium', 'Premium Magic ($299)'),
        ('deluxe', 'Deluxe Party ($399)'),
    ]

    package = forms.ChoiceField(choices=PACKAGE_CHOICES)

    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'date', 'time', 'package', 'message']
        widgets = {
            # Set the min date dynamically
            'date': forms.DateInput(attrs={
                'type': 'date',
                'min': (date.today() + timedelta(days=3)).strftime('%Y-%m-%d')  # Block dates before 3 days in advance
            }),
            'time': forms.TimeInput(attrs={'type': 'time'}),  # Add dropdown for time
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    # Enforce server-side validation for 3-day advance
    def clean_date(self):
        booking_date = self.cleaned_data['date']
        min_date = date.today() + timedelta(days=3)

        if booking_date < min_date:
            raise forms.ValidationError('You must book at least 3 days in advance.')
        return booking_date


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']