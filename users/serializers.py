from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user information.
    Used when showing user profiles or owner details.
    """
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone_number', 'is_gym_owner', 'profile_picture']
        read_only_fields = ['id', 'is_gym_owner']  # These cannot be changed via API


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    is_gym_owner = serializers.BooleanField(default=False, required=False)  
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 
                  'last_name', 'phone_number', 'is_gym_owner']
    
    def validate(self, attrs):
        """
        Check that password and password2 match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        """
        Create and return a new user with hashed password.
        """
        # Remove password2 from the data (not needed for user creation)
        validated_data.pop('password2')
        
        # Create user with hashed password
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate_is_gym_owner(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("is_gym_owner must be a boolean value.")
        return value

class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed user serializer for profile view.
    Shows more information to the authenticated user.
    """
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone_number', 'is_gym_owner', 'profile_picture', 
                  'date_joined', 'last_login']
        read_only_fields = ['id', 'is_gym_owner', 'date_joined', 'last_login']

