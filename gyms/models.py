from django.db import models
from django.conf import settings

class Gym(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gyms')
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=500)
    opening_hours = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='gym_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name