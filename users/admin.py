from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    """Custom admin panel for User model"""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_gym_owner', 'is_staff')
    list_filter = ('is_gym_owner', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'profile_picture', 'is_gym_owner')}),
    )

admin.site.register(User, CustomUserAdmin)