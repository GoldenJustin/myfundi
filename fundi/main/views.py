from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegisterForm, RepairRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import *
from django.contrib.auth.forms import AuthenticationForm

@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()

    if request.method=="POST":
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()
            
    return render(request, 'main/home.html', {'posts': posts})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Check user type and redirect to the respective dashboard
                if hasattr(user, 'carowner'):
                    return redirect('car_owner_dashboard')
                elif Technician.objects.filter(user=user).exists():
                    return redirect('technician_dashboard')
                # Add more user types as needed
                else:
                    # Handle unknown user type
                    return redirect('home')  # Redirect to a default home page or any other appropriate page
            else:
                # Invalid login credentials
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password'})
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})



def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')

    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form" :form})


def logout_user(request):
    logout(request)
    return redirect('home')

# Car owner

@login_required
def dashboard(request):
    # Retrieve repair requests for the logged-in car owner
    car_owner = get_object_or_404(CarOwner, user=request.user)
    repair_requests = RepairRequest.objects.filter(car__owner=request.user.carowner)
    return render(request, 'car_owner/dashboard.html', {'repair_requests': repair_requests})

@login_required
def submit_repair_request(request):
    if request.method == 'POST':
        form = RepairRequestForm(request.POST)
        if form.is_valid():
            repair_request = form.save(commit=False)
            repair_request.car = request.user.carowner.car
            repair_request.save()
            return redirect('car_owner_dashboard')
    else:
        form = RepairRequestForm()
    return render(request, 'car_owner/submit_repair_request.html', {'form': form})




