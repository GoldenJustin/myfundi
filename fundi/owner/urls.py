from django.urls import path
from .views import submit_repair_request, add_car, dashboard

urlpatterns = [
    
    path('owner-dashboard', dashboard, name='owner_dashboard'),
    path('add-car', add_car, name='add-car'),
    path('submit-repair-request', submit_repair_request, name='submit_repair_request'),

]

