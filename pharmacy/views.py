from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from .models import Medicine, Transaction, Prescription, PrescriptionItem
from .forms import AddStockForm, DispenseMedicineForm, PrescriptionForm, PrescriptionItemForm
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.contrib import messages

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
    active_visits = Admission.objects.filter(is_discharged=False).count()
    medicine_alert = low_stock_meds.count()
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

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'quantity', 'price']

@transaction.atomic
def medicine_list(request):
    medicines = Medicine.objects.all().order_by('name')
    add_stock_form = AddStockForm()
    dispense_medicine_form = DispenseMedicineForm()
    total_price = 0
    if request.method == 'POST':
        if 'add_stock' in request.POST:
            add_stock_form = AddStockForm(request.POST)
            if add_stock_form.is_valid():
                medicine_id = request.POST.get('medicine_id')  # Hidden field in template
                medicine = get_object_or_404(Medicine, pk=medicine_id)
                quantity_to_add = add_stock_form.cleaned_data['quantity']
                medicine.quantity += quantity_to_add
                medicine.save()
                # Create transaction
                Transaction.objects.create(medicine=medicine, quantity=quantity_to_add, transaction_type='add_stock')
                add_stock_form = AddStockForm()  # Reset the form
        elif 'dispense_medicine' in request.POST:
            dispense_medicine_form = DispenseMedicineForm(request.POST)
            if dispense_medicine_form.is_valid():
                medicine_id = request.POST.get('medicine_id')  # Hidden field in template
                medicine = get_object_or_404(Medicine, pk=medicine_id)
                quantity_to_dispense = dispense_medicine_form.cleaned_data['quantity']
                if medicine.quantity >= quantity_to_dispense:
                    medicine.quantity -= quantity_to_dispense
                    medicine.save()
                    # Create transaction
                    Transaction.objects.create(medicine=medicine, quantity=-quantity_to_dispense, transaction_type='dispense')
                    dispense_medicine_form = DispenseMedicineForm()  # Reset the form
                else:
                    dispense_medicine_form.add_error(None, "Not enough stock available.")
        else:
            # Handle POS form submission
            any_medicine_selected = False
            for medicine in medicines:
                quantity_str = request.POST.get(f'quantity_{medicine.pk}')
                if quantity_str:
                    try:
                        quantity = int(quantity_str)
                        if quantity > 0:
                            if medicine.quantity >= quantity:
                                total_price += medicine.price * quantity
                                medicine.quantity -= quantity
                                medicine.save()
                                Transaction.objects.create(medicine=medicine, quantity=-quantity, transaction_type='sale')
                                any_medicine_selected = True
                            else:
                                messages.error(request, f'Not enough stock for {medicine.name}. Available stock: {medicine.quantity}')
                    except ValueError:
                        messages.error(request, f'Invalid quantity entered for {medicine.name}')
            if any_medicine_selected:
                messages.success(request, f'Sale complete. Total price: {total_price}')

    for medicine in medicines:
        medicine.stock_status = medicine.get_stock_status_display()
    context = {'medicines': medicines, 'add_stock_form': add_stock_form, 'dispense_medicine_form': dispense_medicine_form, 'total_price': total_price}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'pharmacy/medicine_list.html', context)

def medicine_add(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    context = {'form': form}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'pharmacy/medicine_form.html', context)

def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    context = {'medicine': medicine}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'pharmacy/medicine_detail.html', context)

def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_detail', pk=pk)
    else:
        form = MedicineForm(instance=medicine)
    context = {'form': form, 'medicine': medicine}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'pharmacy/medicine_form.html', context)

def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    context = {'medicine': medicine}
    sidebar = get_sidebar(request)
    if isinstance(sidebar, dict):
        context.update(sidebar)
    return render(request, 'pharmacy/medicine_confirm_delete.html', context)

def pos_view(request):
    medicines = Medicine.objects.all()
    if request.method == 'POST':
        total_price = 0
        for medicine in medicines:
            quantity = request.POST.get(f'quantity_{medicine.pk}')
            if quantity:
                try:
                    quantity = int(quantity)
                    if quantity > 0:
                        if medicine.quantity >= quantity:
                            total_price += medicine.price * quantity
                            medicine.quantity -= quantity
                            medicine.save()
                            Transaction.objects.create(medicine=medicine, quantity=-quantity, transaction_type='sale')
                        else:
                            # Handle insufficient stock
                            return HttpResponse(f'Not enough stock for {medicine.name}')
                except ValueError:
                    # Handle invalid quantity input
                    return HttpResponse('Invalid quantity input')
        # Optionally, redirect to a success page
        return HttpResponse(f'Sale complete. Total price: {total_price}')

    return render(request, 'pharmacy/pos.html', {'medicines': medicines})
