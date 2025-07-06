# /home/ashuranoryoshi/Desktop/hsm/core/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    clinical_summary = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or self.user.username

    class Meta:
        db_table = 'user_profiles'

class UserProfilesEmail(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    clinical_summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            db_table = 'user_profiles_email'