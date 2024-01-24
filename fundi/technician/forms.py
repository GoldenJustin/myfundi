from django import forms
from main.models import Technician

class TechnicianAvailabilityForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ['availability']
