from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *

admin.site.register (CarOwner)
admin.site.register (Technician)
admin.site.register (Car)
admin.site.register (RepairRequest)
admin.site.register (TechnicianAvailability)
admin.site.register (RepairAssignment)
admin.site.register (UserProfile)






