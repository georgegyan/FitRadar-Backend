from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Booking
from .serializers import BookingListSerializer, BookingCreateSerializer, BookingCancelSerializer
from .permissions import IsBookingOwner

class UserBookingsView(generics.ListAPIView):
    """
    API endpoint to list all bookings for the logged-in user.
    """
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only the current user's bookings."""
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date', '-start_time')


class CreateBookingView(generics.CreateAPIView):
    """
    API endpoint to create a new booking.
    """
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Save the booking with the current user."""
        serializer.save(user=self.request.user, status='confirmed')


class CancelBookingView(APIView):
    """
    API endpoint to cancel a booking.
    """
    permission_classes = [permissions.IsAuthenticated, IsBookingOwner]
    
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        
        if booking.status in ['cancelled', 'completed']:
            return Response(
                {"detail": f"Booking already {booking.status}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        
        return Response(
            {"detail": "Booking cancelled successfully."},
            status=status.HTTP_200_OK
        )


class BookingDetailView(generics.RetrieveAPIView):
    """
    API endpoint to view a single booking details.
    """
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingOwner]
    queryset = Booking.objects.all()
    
    def get_queryset(self):
        """Only allow users to view their own bookings."""
        return Booking.objects.filter(user=self.request.user)