from django.db import models
from django.contrib.auth.models import User    

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
class Car(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()

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