from django.shortcuts import render, redirect
from .forms import CustomLoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import *


@login_required(login_url="/sign-in")
def profile(request):            
    return render(request, 'main/users-profile.html',)

def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Redirect users based on their roles
                user_profile = UserProfile.objects.get(user=user)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                elif user_profile.user_type == 'owner':
                    return redirect('owner_dashboard')
                elif user_profile.user_type == 'technician':
                    return redirect('technician_dashboard')
    else:
        form = CustomLoginForm()

    return render(request, 'main/pages-login.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Check user type and create corresponding profile
            user_type = form.cleaned_data['user_type']
            if user_type == 'car_owner':
                car_owner, created = CarOwner.objects.get_or_create(user=user, defaults={'phone_number': form.cleaned_data['phone_number'], 'address': form.cleaned_data['address']})
                if not created:
                    # Update existing CarOwner instance if it already exists
                    car_owner.phone_number = form.cleaned_data['phone_number']
                    car_owner.address = form.cleaned_data['address']
                    car_owner.save()
            elif user_type == 'technician':
                technician, created = Technician.objects.get_or_create(user=user, defaults={'phone_number': form.cleaned_data['phone_number'], 'address': form.cleaned_data['address']})
                if not created:
                    # Update existing Technician instance if it already exists
                    technician.phone_number = form.cleaned_data['phone_number']
                    technician.address = form.cleaned_data['address']
                    technician.save()

            # Create UserProfile
            UserProfile.objects.create(user=user, user_type=user_type)

            # Redirect to a success page or login page
            return redirect('sign-in')
    else:
        form = RegisterForm()

    return render(request, 'main/pages-register.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('sign-in')

def admin_dashboard(request):
    # Add logic specific to the admin dashboard
    return render(request, 'admin/dashboard.html')

def main(request):
    return render(request, 'main/main.html')

