from rest_framework import serializers
from .models import Booking
from gyms.models import Gym

class BookingSerializer(serializers.ModelSerializer):
    gym_name = serializers.CharField(source='gym.name', read_only=True)
    gym_phone = serializers.CharField(source='gym.phone_number', read_only=True)
    gym_address = serializers.CharField(source='gym.address', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'gym', 'gym_name', 'gym_phone', 'gym_address', 'date', 'time', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, data):
        # Optional: check that the gym exists and user is not booking for themselves? Not needed.
        return data