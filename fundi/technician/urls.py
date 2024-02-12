from django.urls import path
from .views import technician_dashboard, update_availability

app_name = 'technician'

urlpatterns = [
    path('technician-dashboard/', technician_dashboard, name='technician_dashboard'),
    path('update-availability/', update_availability, name='update_technician_availability'),

]
