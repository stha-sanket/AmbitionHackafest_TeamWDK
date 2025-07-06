from django.db import models
from patients.models import Patient

# Create your models here.

class Bed(models.Model):
    BED_TYPE_CHOICES = [
        ("Normal", "Normal Bed"),
        ("ICU", "ICU Bed"),
    ]
    bed_number = models.CharField(max_length=10, unique=True)
    bed_type = models.CharField(max_length=10, choices=BED_TYPE_CHOICES)
    is_occupied = models.BooleanField(default=False)
    assigned_patient = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.bed_type} - {self.bed_number} ({'Occupied' if self.is_occupied else 'Available'})"

class BedWaitingList(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    bed_type = models.CharField(max_length=10, choices=Bed.BED_TYPE_CHOICES)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} waiting for {self.bed_type}"
