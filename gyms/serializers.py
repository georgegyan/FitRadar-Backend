from rest_framework import serializers
from .models import Gym
from users.serializers import UserSerializer

class GymListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing gyms (used on the map view).
    Only includes essential fields for performance.
    """
    
    class Meta:
        model = Gym
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 
                  'cover_image', 'price_per_session', 'submission_type']
        read_only_fields = ['id', 'submission_type']


class GymDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for a single gym.
    Includes owner information and booking statistics.
    """
    
    owner = UserSerializer(read_only=True)  # Nested serializer for owner details
    bookings_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Gym
        fields = ['id', 'name', 'description', 'address', 'latitude', 'longitude',
                  'price_per_session', 'price_description', 'cover_image', 'images',
                  'owner', 'submission_type', 'is_active', 'created_at', 'updated_at',
                  'bookings_count']
        read_only_fields = ['id', 'owner', 'submission_type', 'created_at', 'updated_at', 'bookings_count']
    
    def get_bookings_count(self, obj):
        """
        Calculate total confirmed bookings for this gym.
        Used to show popularity.
        """
        return obj.bookings.filter(status='confirmed').count()


class GymCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for gym owners to submit new gyms.
    Automatically sets the owner to the logged-in user.
    """
    
    class Meta:
        model = Gym
        fields = ['name', 'description', 'address', 'latitude', 'longitude',
                  'price_per_session', 'price_description', 'cover_image', 'images']
    
    def validate_latitude(self, value):
        """Validate latitude range (-90 to 90)"""
        if value is not None and (value < -90 or value > 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value
    
    def validate_longitude(self, value):
        """Validate longitude range (-180 to 180)"""
        if value is not None and (value < -180 or value > 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value
    
    def create(self, validated_data):
        """
        Create a new gym with the owner set to the current user.
        """
        request = self.context.get('request')
        validated_data['owner'] = request.user
        validated_data['submission_type'] = 'owner'  # Mark as owner-submitted
        return super().create(validated_data)


class GymUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating gym information.
    Only gym owners or admins can update.
    """
    
    class Meta:
        model = Gym
        fields = ['name', 'description', 'address', 'latitude', 'longitude',
                  'price_per_session', 'price_description', 'cover_image', 'images']