from django import forms
from .models import Medicine, Prescription, PrescriptionItem
from patients.models import Patient
from doctors.models import Doctor

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'quantity', 'price']

class AddStockForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label="Quantity to Add")

class DispenseMedicineForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label="Quantity to Dispense")

class PrescriptionForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), label="Patient")
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), label="Doctor")

    class Meta:
        model = Prescription
        fields = ['patient', 'doctor'] # add more fields as needed


class PrescriptionItemForm(forms.Form):
    medicine = forms.ModelChoiceField(queryset=Medicine.objects.all(), label="Medicine")
    quantity = forms.IntegerField(min_value=1, label="Quantity")
