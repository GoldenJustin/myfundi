from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views import View
from main.forms import CarForm, RepairRequestForm
from main.models import *
from main.forms import RepairRequestForm
from django.db.models import Q

# from django.http import JsonResponse
# from .models import RepairRequest

# Car owner

@login_required
def dashboard(request):
    return render(request, 'main/main.html')


@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user.carowner  # Assuming you have a one-to-one relationship between User and CarOwner
            car.save()
            return redirect('dashboard')  # Replace 'dashboard' with the actual URL name for the owner's dashboard
    else:
        form = CarForm()

    return render(request, 'car_owner/add_car.html', {'form': form})


# @login_required
# def submit_repair_request(request):
#     if request.method == 'POST':
#         form = RepairRequestForm(request.POST)
#         if form.is_valid():
#             repair_request = form.save(commit=False)
#             repair_request.car = request.user.carowner.car
#             repair_request.save()
#             return redirect('car_owner_dashboard')
#     else:
#         form = RepairRequestForm()
#     return render(request, 'car_owner/submit_repair_request.html', {'form': form})

@login_required
class submit_repair_request(View):
    template_name = 'submit_repair_request.html'

    def get(self, request, *args, **kwargs):
        form = RepairRequestForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RepairRequestForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page
        else:
            return render(request, self.template_name, {'form': form})