from django.shortcuts import render, get_object_or_404, redirect
from .models import Bed, BedWaitingList
from django import forms

def get_sidebar(request):
    from patients.models import Patient
    from beds.models import Bed, BedWaitingList
    from pharmacy.models import Medicine
    from bloodbank.models import BloodUnit
    from admissions.models import Admission
    from doctors.models import Doctor
    from django.utils import timezone
    from datetime import timedelta
    from django.db import models
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_beds = Bed.objects.filter(bed_type="Normal").count()
    total_icu = Bed.objects.filter(bed_type="ICU").count()
    available_beds = Bed.objects.filter(bed_type="Normal", is_occupied=False).count()
    available_icu = Bed.objects.filter(bed_type="ICU", is_occupied=False).count()
    low_stock_meds = Medicine.objects.filter(quantity__lt=10)
    near_expiry_meds = Medicine.objects.filter(expiry_date__lte=timezone.now().date() + timedelta(days=30))
    active_visits = Admission.objects.filter(is_discharged=False).count()
    medicine_alert = low_stock_meds.count() + near_expiry_meds.count()
    blood_units = BloodUnit.objects.aggregate(total=models.Sum('quantity'))['total'] or 0
    waiting_count = BedWaitingList.objects.count()
    bed_status = f"{available_beds}/{total_beds}" if total_beds else "0/0"
    icu_status = f"{available_icu}/{total_icu}" if total_icu else "0/0"
    return {
        'patient_count': total_patients,
        'doctor_count': total_doctors,
        'active_visits': active_visits,
        'bed_status': bed_status,
        'icu_status': icu_status,
        'medicine_alert': medicine_alert,
        'blood_units': blood_units,
        'waiting_count': waiting_count,
    }

class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['bed_number', 'bed_type', 'is_occupied', 'assigned_patient']

class BedWaitingForm(forms.ModelForm):
    class Meta:
        model = BedWaitingList
        fields = ['patient', 'bed_type']

def bed_list(request):
    beds = Bed.objects.all().order_by('bed_number')
    context = {'beds': beds}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'beds/bed_list.html', context)

def bed_add(request):
    if request.method == 'POST':
        form = BedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bed_list')
    else:
        form = BedForm()
    context = {'form': form}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'beds/bed_form.html', context)

def bed_detail(request, pk):
    bed = get_object_or_404(Bed, pk=pk)
    context = {'bed': bed}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'beds/bed_detail.html', context)

def bed_edit(request, pk):
    bed = get_object_or_404(Bed, pk=pk)
    if request.method == 'POST':
        form = BedForm(request.POST, instance=bed)
        if form.is_valid():
            form.save()
            return redirect('bed_detail', pk=pk)
    else:
        form = BedForm(instance=bed)
    context = {'form': form, 'bed': bed}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'beds/bed_form.html', context)

def bed_delete(request, pk):
    bed = get_object_or_404(Bed, pk=pk)
    if request.method == 'POST':
        bed.delete()
        return redirect('bed_list')
    context = {'bed': bed}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'beds/bed_confirm_delete.html', context)

def waiting_list(request):
    waiting = BedWaitingList.objects.all().order_by('requested_at')
    context = {'waiting': waiting}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'beds/waiting_list.html', context)

def waiting_add(request):
    if request.method == 'POST':
        form = BedWaitingForm(request.POST)
        if form.is_valid():
            waiting_entry = form.save()
            return redirect('waiting_list')
    else:
        form = BedWaitingForm()
    context = {'form': form}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'beds/waiting_form.html', context)

def waiting_delete(request, pk):
    entry = get_object_or_404(BedWaitingList, pk=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('waiting_list')
    context = {'entry': entry}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'beds/waiting_confirm_delete.html', context)

def icu_list(request):
    icu_beds = Bed.objects.filter(bed_type="ICU").order_by('bed_number')
    context = {'icu_beds': icu_beds}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'beds/icu_list.html', context)
