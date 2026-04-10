from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Gym
from .serializers import GymListSerializer, GymDetailSerializer, GymCreateSerializer, GymUpdateSerializer
from bookings.models import Booking
from bookings.serializers import BookingListSerializer

class NearbyGymsView(generics.ListAPIView):
    """
    API endpoint to get gyms near a location.
    Query params: lat, lng, radius_km (default 5km)
    """
    serializer_class = GymListSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view gyms
    
    def get_queryset(self):
        """
        Filter gyms by proximity to given coordinates.
        Uses simple bounding box for MVP (more accurate would use Haversine formula).
        """
        queryset = Gym.objects.filter(is_active=True)
        
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius_km = self.request.query_params.get('radius_km', 5)
        
        if lat and lng:
            try:
                lat = float(lat)
                lng = float(lng)
                radius_km = float(radius_km)
                
                # Approximate 1 degree latitude = 111 km
                # For longitude, it varies with latitude, but we simplify for MVP
                lat_delta = radius_km / 111.0
                lng_delta = radius_km / (111.0 * abs(lat or 1)) if lat else radius_km / 111.0
                
                queryset = queryset.filter(
                    latitude__gte=lat - lat_delta,
                    latitude__lte=lat + lat_delta,
                    longitude__gte=lng - lng_delta,
                    longitude__lte=lng + lng_delta
                )
            except ValueError:
                pass  # Invalid coordinates, return all active gyms
        
        return queryset


class GymDetailView(generics.RetrieveAPIView):
    """
    API endpoint for detailed view of a single gym.
    """
    queryset = Gym.objects.filter(is_active=True)
    serializer_class = GymDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'


class GymCreateView(generics.CreateAPIView):
    """
    API endpoint for gym owners to submit new gyms.
    """
    serializer_class = GymCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Save the gym with the current user as owner."""
        serializer.save(owner=self.request.user, submission_type='owner')


class GymUpdateView(generics.UpdateAPIView):
    """
    API endpoint for gym owners to update their gym.
    """
    queryset = Gym.objects.all()
    serializer_class = GymUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Only allow owners to update their own gyms."""
        return Gym.objects.filter(owner=self.request.user)


class GymBookingsView(generics.ListAPIView):
    """
    API endpoint to list all bookings for a specific gym.
    Only accessible to the gym owner.
    """
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        gym_id = self.kwargs.get('pk')
        gym = get_object_or_404(Gym, pk=gym_id)
        
        # Only gym owner or admin can view bookings
        if gym.owner != self.request.user and not self.request.user.is_staff:
            return Booking.objects.none()
        
        return Booking.objects.filter(gym=gym).order_by('-booking_date', '-start_time')