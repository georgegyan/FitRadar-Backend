from rest_framework import serializers
from django.utils import timezone
from .models import Booking
from gyms.models import Gym
from gyms.serializers import GymListSerializer

class BookingSerializer(serializers.ModelSerializer):
    """
    Base serializer for booking model.
    """
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'gym', 'booking_date', 'start_time', 
                  'end_time', 'status', 'special_requests', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'created_at']


class BookingListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing bookings (includes gym details).
    Used when a user views their bookings.
    """
    
    gym = GymListSerializer(read_only=True)  # Nested gym info
    
    class Meta:
        model = Booking
        fields = ['id', 'gym', 'booking_date', 'start_time', 'end_time', 
                  'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new booking.
    Includes validation for time slots and availability.
    """
    
    class Meta:
        model = Booking
        fields = ['gym', 'booking_date', 'start_time', 'end_time', 'special_requests']
    
    def validate_gym(self, value):
        """Ensure the gym exists and is active"""
        if not value.is_active:
            raise serializers.ValidationError("This gym is currently not accepting bookings.")
        return value
    
    def validate_booking_date(self, value):
        """Ensure booking date is not in the past"""
        if value < timezone.now().date():
            raise serializers.ValidationError("Cannot book sessions in the past.")
        return value
    
    def validate(self, data):
        """
        Cross-field validation: ensure end time > start time
        and slot is not already booked.
        """
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError({
                "end_time": "End time must be after start time."
            })
        
        # Check for existing booking at same gym, date, and overlapping time
        overlapping = Booking.objects.filter(
            gym=data['gym'],
            booking_date=data['booking_date'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time'],
            status__in=['pending', 'confirmed']
        )
        
        if overlapping.exists():
            raise serializers.ValidationError(
                "This time slot is already booked. Please choose another time."
            )
        
        return data
    
    def create(self, validated_data):
        """
        Create a new booking with the user set to the current user.
        """
        request = self.context.get('request')
        validated_data['user'] = request.user
        validated_data['status'] = 'confirmed'  # For MVP, auto-confirm (no payment)
        return super().create(validated_data)


class BookingCancelSerializer(serializers.Serializer):
    """
    Simple serializer for cancel action (no data needed, just the endpoint).
    Used to document the cancel operation.
    """
    pass