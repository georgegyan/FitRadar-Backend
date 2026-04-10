from django.urls import path
from .views import UserBookingsView, CreateBookingView, CancelBookingView, BookingDetailView

urlpatterns = [
    path('', UserBookingsView.as_view(), name='user-bookings'),
    path('create/', CreateBookingView.as_view(), name='create-booking'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('<int:pk>/cancel/', CancelBookingView.as_view(), name='cancel-booking'),
]