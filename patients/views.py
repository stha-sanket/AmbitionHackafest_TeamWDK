from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient
from django import forms
from core.views import dashboard  # for sidebar context

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'sex', 'address', 'phone', 'guardian_name', 'guardian_phone', 'medical_history', 'diagnosis_report']

# Helper to get sidebar context
from core.views import dashboard as get_sidebar_context

def get_sidebar(request):
    # Instead of calling the dashboard view directly, reconstruct the context here
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

def patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')
    context = {'patients': patients}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'patients/patient_list.html', context)

def patient_add(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    context = {'form': form}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'patients/patient_form.html', context)

def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    context = {'patient': patient}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'patients/patient_detail.html', context)

def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', pk=pk)
    else:
        form = PatientForm(instance=patient)
    context = {'form': form, 'patient': patient}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'patients/patient_form.html', context)

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    context = {'patient': patient}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'patients/patient_confirm_delete.html', context)

def diagnosis_report_list(request):
    patients = Patient.objects.exclude(diagnosis_report__exact='').order_by('-created_at')
    context = {'patients': patients}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'patients/diagnosis_report_list.html', context)
