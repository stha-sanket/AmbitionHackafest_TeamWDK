from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from beds.models import Bed

# Create your models here.

class Admission(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctors = models.ManyToManyField(Doctor)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    diagnosis_notes = models.TextField()
    admitted_at = models.DateTimeField(auto_now_add=True)
    discharged_at = models.DateTimeField(blank=True, null=True)
    is_discharged = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ("critical", "Critical"),
        ("normal", "Normal"),
        ("discharged", "Discharged"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="normal")

    def discharge_summary(self):
        return f"Patient: {self.patient.name}\nDoctors: {', '.join([d.name for d in self.doctors.all()])}\nBed: {self.bed.bed_number}\nDiagnosis: {self.diagnosis_notes}\nAdmitted: {self.admitted_at}\nDischarged: {self.discharged_at}"

    def __str__(self):
        return f"{self.patient.name} - {'Discharged' if self.is_discharged else 'Admitted'}"
