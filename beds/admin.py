from django.contrib import admin
from .models import Bed, BedWaitingList

# Register your models here.
admin.site.register(Bed)
admin.site.register(BedWaitingList)
