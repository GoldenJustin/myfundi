from django.urls import path
from . import views
from owner.views import dashboard, submit_repair_request, add_car
from technician.views import technician_dashboard
from .views import admin_dashboard, main



urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('sign-in', views.custom_login, name='sign-in'),
    path('register', views.sign_up, name='sign_up'),
    path('logout', views.logout_user, name='logout'),
    path('owner-dashboard', dashboard, name='owner_dashboard'),
    path('add-car', add_car, name='add-car'),
    path('submit-repair-request', submit_repair_request, name='submit_repair_request'),

    path('technician/dashboard/', technician_dashboard, name='technician_dashboard'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('', main, name='main'),

]

