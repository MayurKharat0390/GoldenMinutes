from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin with role and location fields
    """
    list_display = ['username', 'email', 'role', 'phone_number', 'terms_accepted', 'created_at']
    list_filter = ['role', 'terms_accepted', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'phone_number']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Profile', {
            'fields': ('role', 'phone_number', 'profile_picture')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'location_updated_at')
        }),
        ('Legal & Consent', {
            'fields': ('terms_accepted', 'terms_accepted_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'location_updated_at', 'terms_accepted_at']
