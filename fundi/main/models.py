from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _  

class CarOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    availability = models.CharField(max_length=255, blank=True, null=True)  # You can adjust this field based on your requirements

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('owner', 'Car Owner'),
        ('technician', 'Technician'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
    
# Model for Cars

def validate_license_plate_number(value):
    # Check if the license plate number follows the specified format
    if not (
        value.startswith('T') and
        len(value) == 7 and
        value[1:4].isdigit() and
        value[4].isalpha() and
        'A' <= value[4] <= 'E' and
        value[5:].isalpha()
    ):
        raise ValidationError(
            _('%(value)s is not a valid license plate number. It should start with T followed by three digits, and three letters with the first letter in the range A to E.'),
            params={'value': value},
        )

class Car(models.Model):
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
    ]
    TRANSMISSION_TYPE_CHOICES=[
        ('manual', 'Manual Transmission'),
        ('automatic', 'Automatic Transmission'),
    ]
    owner = models.ForeignKey('CarOwner', on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=50, null=True, blank=True)
    license_plate_number = models.CharField(
        max_length=7,
        unique=True,
        validators=[validate_license_plate_number],
        help_text="Enter a license plate number starting with 'T' followed by three digits, and three letters.",
    )
    mileage = models.PositiveIntegerField(default=0)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    transmission_type = models.CharField(max_length=20, choices=TRANSMISSION_TYPE_CHOICES)
    next_service_due = models.DateField(null=True, blank=True)
    last_service_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.make} {self.model} {self.year} - {self.license_plate_number}"

    def save(self, *args, **kwargs):
        # Add 'T' to the beginning if not already present
        if not self.license_plate_number.startswith('T'):
            self.license_plate_number = f'T{self.license_plate_number}'
        # Convert letters to uppercase
        self.license_plate_number = self.license_plate_number.upper()
        super().save(*args, **kwargs)


class RepairRequest(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=255)  
    license_plate = models.CharField(max_length=20) 
    issue_description = models.TextField()  
    additional_comments = models.TextField()  
    repair_type = models.CharField(max_length=255)  
    preferred_date = models.DateField()  
    request_time = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    owner_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    owner_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f'Repair Request for {self.car_model} - {self.request_time}'
    
    
# Model for Technician Availability
class TechnicianAvailability(models.Model):
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    available_time = models.DateTimeField()
    technician_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    technician_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

# Model for Repair Assignments
class RepairAssignment(models.Model):
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    repair_request = models.OneToOneField(RepairRequest, on_delete=models.CASCADE)
    assignment_time = models.DateTimeField(auto_now_add=True)
    completion_time = models.DateTimeField(null=True, blank=True)