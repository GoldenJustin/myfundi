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
            
    return render(request, 'main/user.html', {'posts': posts})


# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)

#                 # Check user type and redirect to the respective dashboard
#                 if hasattr(user, 'carowner'):
#                     return redirect('car_owner_dashboard')
#                 elif Technician.objects.filter(user=user).exists():
#                     return redirect('technician_dashboard')
#                 # Add more user types as needed
#                 else:
#                     # Handle unknown user type
#                     return redirect('home')  # Redirect to a default home page or any other appropriate page
#             else:
#                 # Invalid login credentials
#                 return render(request, 'pages-login.html', {'form': form, 'error_message': 'Invalid username or password'})
#     else:
#         form = AuthenticationForm()

#     return render(request, 'pages-login.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or home
                return redirect('home')
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

