from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    user_type = forms.ChoiceField(choices=[('car_owner', 'Car Owner'), ('technician', 'Technician')], required=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "address", "password1", "password2", "user_type"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            # Check user type and create corresponding profile
            user_type = self.cleaned_data['user_type']
            if user_type == 'car_owner':
                CarOwner.objects.create(user=user, phone_number=self.cleaned_data['phone_number'], address=self.cleaned_data['address'])
            elif user_type == 'technician':
                Technician.objects.create(user=user, phone_number=self.cleaned_data['phone_number'], address=self.cleaned_data['address'])

        return user

class RepairRequestForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ['description', 'owner_latitude', 'owner_longitude']

    def __init__(self, *args, **kwargs):
        super(RepairRequestForm, self).__init__(*args, **kwargs)
        self.fields['owner_latitude'].widget.attrs['readonly'] = True
        self.fields['owner_longitude'].widget.attrs['readonly'] = True


class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

