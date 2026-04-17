from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Gym
from .serializers import GymSerializer

class GymListCreateView(generics.ListCreateAPIView):
    queryset = Gym.objects.all().order_by('-created_at')
    serializer_class = GymSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_gym_owner:
            raise PermissionDenied("Only gym owners can create gyms.")
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]