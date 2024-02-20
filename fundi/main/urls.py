from django.urls import path
from . import views
from technician.views import technician_dashboard
from .views import admin_dashboard, main



urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('sign-in', views.custom_login, name='sign-in'),
    path('register', views.sign_up, name='sign_up'),
    path('logout', views.logout_user, name='logout'),
  

    path('technician/dashboard/', technician_dashboard, name='technician_dashboard'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('', main, name='main'),

]

