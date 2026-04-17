from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_gym_owner']
        extra_kwargs = {
            'email': {'required': True},
            'is_gym_owner': {'required': True}
        }
    
    def create(self, validated_data):
        user = User.objcts.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_gym_owner=validated_data['is_gym_owner']
        )
        return user