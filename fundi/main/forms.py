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

# class RepairRequestForm(forms.ModelForm):
#     class Meta:
#         model = RepairRequest
#         fields = [
#             'car_model',
#             'license_plate',
#             'issue_description',
#             'additional_comments',
#             'repair_type',
#             'preferred_date',
#         ]


class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'color', 'license_plate_number', 'mileage', 'fuel_type', 'transmission_type', 'next_service_due', 'last_service_date']


class RepairRequestForm(forms.ModelForm):
    car_model = forms.CharField(max_length=255, required=False)
    license_plate = forms.CharField(max_length=20)

    class Meta:
        model = RepairRequest
        fields = ['car_model', 'license_plate', 'issue_description', 'additional_comments', 'repair_type', 'preferred_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set initial values based on license_plate
        license_plate = self.initial.get('license_plate', None)
        if license_plate:
            try:
                car = Car.objects.get(license_plate_number=license_plate)
                self.initial['car_model'] = car.model
                self.initial['year'] = car.year
                self.initial['color'] = car.color
                self.initial['fuel_type'] = car.fuel_type
                self.initial['transmission_type'] = car.transmission_type
                # Add more initial values here based on the car object
            except Car.DoesNotExist:
                pass


