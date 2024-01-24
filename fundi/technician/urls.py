from django.urls import path
from .views import dashboard, update_availability

app_name = 'technician'

urlpatterns = [
    path('technician-dashboard/', dashboard, name='technician_dashboard'),
    path('update-availability/', update_availability, name='update_technician_availability'),

]
