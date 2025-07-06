from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import BloodUnit
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
    available_icu = Bed.objects.filter(bed_type="ICU").count()
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

class BloodUnitForm(forms.ModelForm):
    class Meta:
        model = BloodUnit
        fields = ['blood_group', 'quantity']

from django.contrib import messages
from django.db import transaction

@transaction.atomic
def bloodunit_list(request):
    bloodunits = BloodUnit.objects.all().order_by('blood_group')
    selected_bloodunit = None
    if request.method == 'POST':
        selected_bloodunit_id = request.POST.get('selected_bloodunit')
        selected_bloodunit_id = request.POST.get('selected_bloodunit')

        if 'edit_bloodunit' in request.POST:
            if selected_bloodunit_id:
                return HttpResponseRedirect(reverse('bloodunit_edit', args=[selected_bloodunit_id]))
            else:
                messages.error(request, 'Please select a blood unit to edit.')
        elif 'delete_bloodunit' in request.POST:
            if selected_bloodunit_id:
                return HttpResponseRedirect(reverse('bloodunit_delete', args=[selected_bloodunit_id]))
            else:
                messages.error(request, 'Please select a blood unit to delete.')
        # Dispense blood
        else:
            if selected_bloodunit_id:
                selected_bloodunit = get_object_or_404(BloodUnit, pk=selected_bloodunit_id)
                for bloodunit in bloodunits:
                    quantity_str = request.POST.get(f'quantity_{bloodunit.pk}')
                    if quantity_str:
                        try:
                            quantity = int(quantity_str)
                            if quantity > 0:
                                if bloodunit.quantity >= quantity:
                                    bloodunit.quantity -= quantity
                                    bloodunit.save()
                                    messages.success(request, f'{quantity} unit(s) of {bloodunit.blood_group} dispensed successfully.')
                                else:
                                    messages.error(request, f'Not enough {bloodunit.blood_group} available. Available: {bloodunit.quantity}')
                        except ValueError:
                            messages.error(request, f'Invalid quantity for {bloodunit.blood_group}.')
            else:
                messages.error(request, 'Please select a blood unit to dispense from.')

    bloodunits = BloodUnit.objects.all().order_by('blood_group')
    context = {'bloodunits': bloodunits}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'bloodbank/bloodunit_list.html', context)
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'bloodbank/bloodunit_list.html', context)

def bloodunit_add(request):
    if request.method == 'POST':
        form = BloodUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bloodunit_list')
    else:
        form = BloodUnitForm()
    context = {'form': form}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'bloodbank/bloodunit_form.html', context)

def bloodunit_detail(request, pk):
    bloodunit = get_object_or_404(BloodUnit, pk=pk)
    context = {'bloodunit': bloodunit}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'bloodbank/bloodunit_detail.html', context)

def bloodunit_edit(request, pk):
    bloodunit = get_object_or_404(BloodUnit, pk=pk)
    if request.method == 'POST':
        form = BloodUnitForm(request.POST, instance=bloodunit)
        if form.is_valid():
            form.save()
            return redirect('bloodunit_detail', pk=pk)
    else:
        form = BloodUnitForm(instance=bloodunit)
    context = {'form': form, 'bloodunit': bloodunit}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'bloodbank/bloodunit_form.html', context)

def bloodunit_delete(request, pk):
    bloodunit = get_object_or_404(BloodUnit, pk=pk)
    if request.method == 'POST':
        bloodunit.delete()
        return redirect('bloodunit_list')
    context = {'bloodunit': bloodunit}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'bloodbank/bloodunit_confirm_delete.html', context)
