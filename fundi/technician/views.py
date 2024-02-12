from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.models import RepairRequest, Technician
from .forms import TechnicianAvailabilityForm

@login_required
def technician_dashboard(request):
    # Retrieve repair assignments for the logged-in technician
    return render(request, 'technician/dashboard.html')

@login_required
def update_availability(request):
    if request.method == 'POST':
        form = TechnicianAvailabilityForm(request.POST)
        if form.is_valid():
            technician = request.user.technician
            technician.availability = form.cleaned_data['availability']
            technician.save()
            return redirect('technician_dashboard')
    else:
        form = TechnicianAvailabilityForm()
    return render(request, 'technician/update_availability.html', {'form': form})
