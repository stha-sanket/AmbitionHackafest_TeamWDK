from django.shortcuts import render, get_object_or_404, redirect
from .models import Doctor
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

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'department', 'specialization', 'availability']

def doctor_list(request):
    doctors = Doctor.objects.all().order_by('-created_at')
    context = {'doctors': doctors}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'doctors/doctor_list.html', context)

def doctor_add(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    context = {'form': form}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'doctors/doctor_form.html', context)

def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    context = {'doctor': doctor}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'doctors/doctor_detail.html', context)

def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_detail', pk=pk)
    else:
        form = DoctorForm(instance=doctor)
    context = {'form': form, 'doctor': doctor}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'doctors/doctor_form.html', context)

def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')
    context = {'doctor': doctor}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'doctors/doctor_confirm_delete.html', context)
