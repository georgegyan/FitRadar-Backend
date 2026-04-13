from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Gym
from .serializers import GymListSerializer, GymDetailSerializer, GymCreateSerializer, GymUpdateSerializer
from bookings.models import Booking
from bookings.serializers import BookingListSerializer
from .permissions import IsGymOwner
from users.permissions import IsOwnerOrReadOnly

class GymListCreateView(generics.ListCreateAPIView):
    queryset = Gym.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsGymOwner]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GymCreateSerializer
        return GymListSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_gym_owner:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only gym owners can submit gyms.")
        serializer.save()

class NearbyGymsView(generics.ListAPIView):
    serializer_class = GymListSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view gyms
    
    def get_queryset(self):
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
    queryset = Gym.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return GymCreateSerializer  # reuse same serializer for updates
        return GymDetailSerializer

class GymCreateView(generics.CreateAPIView):
    serializer_class = GymCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Save the gym with the current user as owner."""
        serializer.save(owner=self.request.user, submission_type='owner')

class GymUpdateView(generics.UpdateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Only allow owners to update their own gyms."""
        return Gym.objects.filter(owner=self.request.user)

class GymBookingsView(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        gym_id = self.kwargs.get('pk')
        gym = get_object_or_404(Gym, pk=gym_id)
        
        # Only gym owner or admin can view bookings
        if gym.owner != self.request.user and not self.request.user.is_staff:
            return Booking.objects.none()
        
        return Booking.objects.filter(gym=gym).order_by('-booking_date', '-start_time')