from django.urls import path
from .views import NearbyGymsView, GymDetailView, GymCreateView, GymUpdateView, GymBookingsView

urlpatterns = [
    path('', NearbyGymsView.as_view(), name='gym-list'),  # GET /api/gyms/?lat=...&lng=...
    path('create/', GymCreateView.as_view(), name='gym-create'),
    path('<int:pk>/', GymDetailView.as_view(), name='gym-detail'),
    path('<int:pk>/update/', GymUpdateView.as_view(), name='gym-update'),
    path('<int:pk>/bookings/', GymBookingsView.as_view(), name='gym-bookings'),
]