from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.db import models
from django.contrib import messages
from .models import Admission
from patients.models import Patient
from doctors.models import Doctor
from beds.models import Bed, BedWaitingList
from pharmacy.models import Medicine
from bloodbank.models import BloodUnit
from django.utils import timezone
from datetime import timedelta

def get_sidebar(request):
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

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['patient', 'doctors', 'bed', 'diagnosis_notes', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['bed'].queryset = Bed.objects.filter(models.Q(is_occupied=False) | models.Q(pk=self.instance.bed.pk))
        else:
            self.fields['bed'].queryset = Bed.objects.filter(is_occupied=False)

def admission_list(request):
    admissions = Admission.objects.all().order_by('-admitted_at')
    context = {'admissions': admissions}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'admissions/admission_list.html', context)

def admission_add(request):
    form = AdmissionForm(request.POST or None)

    # Get all waiting patients from BedWaitingList
    waiting_patients = BedWaitingList.objects.select_related('patient').all()

    # Extract patient IDs already in the waiting list
    waiting_ids = [wp.patient.pk for wp in waiting_patients]

    # Non-waiting patients for dropdown
    non_waiting_patients = form.fields['patient'].queryset.exclude(pk__in=waiting_ids)

    if request.method == "POST" and form.is_valid():
        admission = form.save(commit=False)  # Get the admission object without saving
        bed = form.cleaned_data['bed']  # Get the selected bed from the form
        patient = form.cleaned_data['patient']  # Get the selected patient from the form

        # Update bed status and assigned patient
        bed.is_occupied = True
        bed.assigned_patient = patient.name  # Assuming patient has a 'name' field
        bed.save()

        # Save the admission object
        admission.patient = patient  # Set patient relationship explicitly
        admission.bed = bed  # Set bed relationship explicitly
        admission.save()
        form.save_m2m()  # Save ManyToMany relationships (for doctors)

        messages.success(request, 'Admission created successfully.')
        return redirect('admission_list')

    context = {
        'form': form,
        'admission': None,
        'waiting_patients': waiting_patients,
        'non_waiting_patients': non_waiting_patients,
    }

    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)

    return render(request, 'admissions/admission_form.html', context)

def admission_detail(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    context = {'admission': admission}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'admissions/admission_detail.html', context)

def admission_edit(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    old_bed = admission.bed
    if request.method == 'POST':
        form = AdmissionForm(request.POST, instance=admission)
        if form.is_valid():
            admission = form.save()
            new_bed = admission.bed
            if old_bed != new_bed:
                old_bed.is_occupied = False
                old_bed.assigned_patient = None
                old_bed.save()
                new_bed.is_occupied = True
                new_bed.assigned_patient = admission.patient.name
                new_bed.save()
            return redirect('admission_detail', pk=pk)
    else:
        form = AdmissionForm(instance=admission)

    context = {'form': form, 'admission': admission}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'admissions/admission_form.html', context)

def admission_discharge(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    if request.method == 'POST':
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        admission.is_discharged = True
        admission.discharged_at = timezone.now()
        admission.save()

        bed = admission.bed
        if bed:
            bed.is_occupied = False
            bed.assigned_patient = None
            bed.save()

            waiting_entry = BedWaitingList.objects.filter(
                bed_type=bed.bed_type
            ).order_by('requested_at').first()

            if waiting_entry:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "bed_notifications",
                    {
                        "type": "bed_available_notification",
                        "message": f"A {bed.bed_type} is now available for {waiting_entry.patient.name}."
                    }
                )

        return redirect('admission_detail', pk=pk)

    context = {'admission': admission}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'admissions/admission_discharge.html', context)

def admission_delete(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    if request.method == 'POST':
        admission.delete()
        return redirect('admission_list')
    context = {'admission': admission}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'admissions/admission_confirm_delete.html', context)

def hospital_visits(request):
    visits = Admission.objects.filter(is_discharged=False).order_by('-admitted_at')
    context = {'visits': visits}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'admissions/visit_list.html', context)
