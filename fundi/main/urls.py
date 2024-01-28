from django.urls import path
from . import views
from owner.views import dashboard, submit_repair_request



urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('logout', views.logout_user, name='logout'),
    path('owner-dashboard/', dashboard, name='car_owner_dashboard'),
    path('submit-repair-request/', submit_repair_request, name='submit_repair_request'),

]

