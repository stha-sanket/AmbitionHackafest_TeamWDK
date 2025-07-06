from django.db import models
from patients.models import Patient  # Import the Patient model
from doctors.models import Doctor # Import the Doctor model

# Create your models here.

class Medicine(models.Model):
    STOCK_STATUS_CHOICES = [
        ("full", "Full"),
        ("need", "Need Stock"),
        ("out", "Out of Stock"),
    ]
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)  # <-- ADDED THIS LINE
    expiry_date = models.DateField(blank=True, null=True)                  # <-- ADDED THIS LINE
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    stock_status = models.CharField(max_length=10, choices=STOCK_STATUS_CHOICES, default="full")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} ({self.quantity} units)"

    def get_stock_status_display(self):
        # NOTE: There might be a logic issue here. For any positive quantity,
        # self.quantity is never less than (self.quantity * 0.45).
        # You may want a fixed threshold, e.g., `elif self.quantity < 20:`
        if self.quantity == 0:
            return "Out of Stock"
        elif self.quantity < (self.quantity * 0.45):
            return "Need Stock"
        else:
            return "Full"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('add_stock', 'Add Stock'),
        ('dispense', 'Dispense'),
    ]

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='transactions')
    quantity = models.IntegerField()  # Positive for adding, negative for dispensing
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # Uncomment after creating users app

    def __str__(self):
        return f"{self.transaction_type} - {self.medicine.name} - {self.quantity}"

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    prescription_date = models.DateField(auto_now_add=True)
    # Add other prescription details here, e.g., diagnosis, notes

    def __str__(self):
        return f"Prescription for {self.patient.name} by Dr. {self.doctor.name} on {self.prescription_date}"

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    # Add any additional item details here, e.g., dosage instructions
    def __str__(self):
        return f"{self.medicine.name} - {self.quantity}"