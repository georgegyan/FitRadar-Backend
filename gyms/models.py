from django.db import models
from django.conf import settings

class Gym(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    price_per_session = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price_description = models.CharField(max_length=200, blank=True)
    cover_image = models.ImageField(upload_to='gym_covers/', blank=True, null=True)
    images = models.JSONField(default=list, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_gyms')
    submission_type = models.CharField(max_length=10, choices=[('owner', 'Owner Submitted'), ('admin', 'Admin Added')], default='owner')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gyms'
        ordering = ['-created_at']

    def __str__(self):
        return self.name