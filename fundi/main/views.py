from django.shortcuts import get_object_or_404, render, redirect
from .forms import CustomLoginForm, RegisterForm, RepairRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import *
from django.contrib.auth.forms import AuthenticationForm

@login_required(login_url="/sign-in")
def home(request):
    posts = Post.objects.all()

    if request.method=="POST":
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()
            
    return render(request, 'main/base.html', {'posts': posts})

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
            login(request, user)
            return redirect('/home')

    else:
        form = RegisterForm()

    return render(request, 'main/pages-register.html', {"form" :form})

def logout_user(request):
    logout(request)
    return redirect('sign-in')

def admin_dashboard(request):
    # Add logic specific to the admin dashboard
    return render(request, 'admin/dashboard.html')

def main(request):
    return render(request, 'main/main.html')

