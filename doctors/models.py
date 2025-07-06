from django.db import models

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    availability = models.CharField(max_length=100, help_text="e.g. Mon-Fri 9am-5pm")
    assigned_patients = models.TextField(blank=True, help_text="Comma-separated patient IDs or names")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"
