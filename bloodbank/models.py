from django.db import models

# Create your models here.

class BloodUnit(models.Model):
    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-")
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blood_group}: {self.quantity} units"
