from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from main.forms import RepairRequestForm
from main.models import *

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




