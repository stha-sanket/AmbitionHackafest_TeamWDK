from django.contrib import admin
from .models import UserProfile, UserProfilesEmail

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'age', 'sex', 'blood_group', 'phone', 'updated_at')
    search_fields = ('user__username', 'name', 'phone', 'blood_group')
    list_filter = ('sex', 'blood_group', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserProfilesEmail)
class UserProfilesEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'age', 'sex', 'blood_group', 'phone', 'updated_at')
    search_fields = ('email', 'name', 'phone')
    list_filter = ('sex', 'blood_group', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
