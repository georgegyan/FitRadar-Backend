from rest_framework import serializers
from .models import Gym

class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['id', 'owner', 'name', 'description', 'address', 'phone_number',
                  'opening_hours', 'image', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']