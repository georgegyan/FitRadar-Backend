from rest_framework import serializers
from .models import Gym
from users.serializers import UserSerializer

class GymListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 
                  'cover_image', 'price_per_session', 'submission_type']
        read_only_fields = ['id', 'submission_type']


class GymDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')  # Display owner's username
    # bookings_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Gym
        fields = '__all__'  # Show all fields for detailed view
        read_only_fields = ['id', 'owner_username', 'submission_type', 'created_at', 'updated_at', 'bookings_count']
    
    def get_bookings_count(self, obj):
        return obj.bookings.filter(status='confirmed').count()

class GymCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['name', 'description', 'address', 
                  'price_per_session', 'price_description', 'cover_image', 'images']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        validated_data['submission_type'] = 'owner'  # Mark as owner-submitted
        return super().create(validated_data)

class GymUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['name', 'description', 'address', 'latitude', 'longitude',
                  'price_per_session', 'price_description', 'cover_image', 'images']