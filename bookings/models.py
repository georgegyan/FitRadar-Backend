from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

class Booking(models.Model):
    """
    Model representing a gym session booking.
    Users can book time slots at specific gyms.
    """
    
    # Status choices for booking workflow
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="User who made the booking"
    )
    
    gym = models.ForeignKey(
        'gyms.Gym',
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="Gym being booked"
    )
    
    # Booking Details
    booking_date = models.DateField(help_text="Date of the booking")
    start_time = models.TimeField(help_text="Start time of the session")
    end_time = models.TimeField(help_text="End time of the session")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Additional Info
    special_requests = models.TextField(blank=True, help_text="Any special requests from the user")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        ordering = ['-booking_date', '-start_time']  # Most recent first
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        # Prevent double-booking the same time slot at the same gym
        unique_together = ['gym', 'booking_date', 'start_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.gym.name} on {self.booking_date}"
    
    def clean(self):
        """
        Custom validation for bookings.
        Called automatically before saving.
        """
        # Check if end time is after start time
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")
        
        # Check if booking date is not in the past
        if self.booking_date < timezone.now().date():
            raise ValidationError("Cannot book sessions in the past")
        
        # Check for overlapping bookings at the same gym
        overlapping = Booking.objects.filter(
            gym=self.gym,
            booking_date=self.booking_date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
            status__in=['pending', 'confirmed']  # Only active bookings count
        )
        
        # Exclude current booking when updating
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
        
        if overlapping.exists():
            raise ValidationError("This time slot is already booked")
    
    def save(self, *args, **kwargs):
        """Override save to run validation"""
        self.clean()
        super().save(*args, **kwargs)
    
    def cancel(self):
        """Method to cancel a booking"""
        if self.status not in ['cancelled', 'completed']:
            self.status = 'cancelled'
            self.save()
            return True
        return False