from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Gym(models.Model):
    name = models.CharField(max_length=200, help_text="Gym name")
    description = models.TextField(blank=True, help_text="Detailed description of the gym")
    #Location
    address = models.TextField(help_text="Full address of the gym")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    #Pricing
    price_per_session = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price_description = models.CharField(max_length=200, blank=True, help_text="e.g, 'Pay per session' or 'Monthly membership'")
    #Media
    cover_image = models.ImageField(upload_to='gym_covers/', blank=True, null=True)
    images = models.JSONField(default=list, blank=True, help_text="List of image URLS")
    #Owner Information
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_gyms',
        help_text="User who submitted/owns this gym"
    )
    #Submission Type
    SUBMISSION_TYPES = [
        ('gps', 'GPS Detected'),
        ('owner', 'Owner Submitted'),
        ('admin', 'Admin Added'),
    ]
    submission_type = models.CharField(max_length=10, choices=SUBMISSION_TYPES, default='owner')
    
    # Metadata
    is_active = models.BooleanField(default=True, help_text="Whether this gym is currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'gyms'
        ordering = ['-created_at']  # Newest first
        verbose_name = 'Gym'
        verbose_name_plural = 'Gyms'
    
    def __str__(self):
        return self.name
    
    def get_coordinates(self):
        """Return coordinates as a tuple for map display"""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None