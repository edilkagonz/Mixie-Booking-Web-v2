from django import forms
from datetime import date, timedelta
from .models import Booking
from .models import Contact, Package
from django import forms
from .models import Booking, DataRequest
from datetime import date, timedelta

class BookingForm(forms.ModelForm):
    consent = forms.BooleanField(required=True, label="I agree to the Terms and Privacy Policy.")

    package = forms.ModelChoiceField(
        queryset=Package.objects.filter(is_active=True),
        empty_label=None,  # Removes the default "Select a package" placeholder
        label="🎁 Select Package",
        to_field_name="id",
    )

    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'date', 'time', 'package', 'message']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'min': (date.today() + timedelta(days=3)).strftime('%Y-%m-%d')
            }),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        # Get the selected package (if any) from the view
        selected_package = kwargs.pop('selected_package', None)
        super().__init__(*args, **kwargs)

        # Set label format for dropdown
        self.fields['package'].label_from_instance = lambda obj: f"{obj.name} - ${obj.price} ({obj.duration})"

        # Ensure 'Select a package' appears when no package is preselected
        self.fields['package'].empty_label = "Select a Package"  # Adds a blank choice

        # Preselect the package if provided, otherwise force it blank
        if selected_package:
            self.fields['package'].initial = selected_package.id
        else:
            self.fields['package'].initial = None  # No default selection




class ContactForm(forms.ModelForm):
    consent = forms.BooleanField(required=True, label="I agree to the Privacy Policy.")

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

class DataRequestForm(forms.ModelForm):
    class Meta:
        model = DataRequest
        fields = ['name', 'email', 'request_type', 'reason']