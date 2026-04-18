from django.db import models
from django.conf import settings
from gyms.models import Gym

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('gym', 'date', 'time')

        def __str__(self):
            return f"{self.user.username} booked {self.gym.name} on {self.date} at {self.time}"