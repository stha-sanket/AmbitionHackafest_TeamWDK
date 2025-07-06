from django.db import models

# Create your models here.

class Patient(models.Model):
    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=20)
    medical_history = models.TextField(blank=True)
    diagnosis_report = models.TextField(blank=True, help_text="Diagnosis report or file path")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (ID: {self.pk})"
