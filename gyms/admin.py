from django.contrib import admin
from .models import Gym

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'owner', 'submission_type', 'is_active', 'created_at')
    list_filter = ('submission_type', 'is_active', 'created_at')
    search_fields = ('name', 'address', 'owner__username', 'owner__email')
    list_editable = ('is_active',)  # Can toggle active status directly from list view
    readonly_fields = ('created_at', 'updated_at')