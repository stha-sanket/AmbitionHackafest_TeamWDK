from django.shortcuts import render
from patients.models import Patient
from beds.models import Bed, BedWaitingList
from pharmacy.models import Medicine
from bloodbank.models import BloodUnit
from admissions.models import Admission
from doctors.models import Doctor
from django.utils import timezone
from datetime import timedelta
from django.db import models

# Create your views here.

def dashboard(request):
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_beds = Bed.objects.filter(bed_type="Normal").count()
    total_icu = Bed.objects.filter(bed_type="ICU").count()
    available_beds = Bed.objects.filter(bed_type="Normal", is_occupied=False).count()
    available_icu = Bed.objects.filter(bed_type="ICU", is_occupied=False).count()
    occupied_beds = total_beds - available_beds
    occupied_icu = total_icu - available_icu
    low_stock_meds = Medicine.objects.filter(quantity__lt=10)
    low_blood = BloodUnit.objects.filter(quantity__lt=5)
    recent_admissions = Admission.objects.order_by('-admitted_at')[:5]
    recent_discharges = Admission.objects.filter(is_discharged=True).order_by('-discharged_at')[:5]
    active_visits = Admission.objects.filter(is_discharged=False).count()
    medicine_alert = low_stock_meds.count()
    blood_units = BloodUnit.objects.aggregate(total=models.Sum('quantity'))['total'] or 0
    waiting_count = BedWaitingList.objects.count()
    bed_status = f"{available_beds}/{total_beds}" if total_beds else "0/0"
    icu_status = f"{available_icu}/{total_icu}" if total_icu else "0/0"
    context = {
        'total_patients': total_patients,
        'total_beds': total_beds,
        'total_icu': total_icu,
        'available_beds': available_beds,
        'available_icu': available_icu,
        'occupied_beds': occupied_beds,
        'occupied_icu': occupied_icu,
        'low_stock_meds': low_stock_meds,
        'low_blood': low_blood,
        'recent_admissions': recent_admissions,
        'recent_discharges': recent_discharges,
        # Sidebar dynamic counts
        'patient_count': total_patients,
        'doctor_count': total_doctors,
        'active_visits': active_visits,
        'bed_status': bed_status,
        'icu_status': icu_status,
        'medicine_alert': medicine_alert,
        'blood_units': blood_units,
        'waiting_count': waiting_count,
    }
    return render(request, 'core/dashboard.html', context)