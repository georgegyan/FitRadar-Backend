from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Gym
from .serializers import GymSerializer

class GymListCreateView(generics.ListCreateAPIView):
    queryset = Gym.objects.all().order_by('-created_at')
    serializer_class = GymSerializer

    def perform_create(self, serializer):
        # Only authenticated users can create, and we set owner to current user
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]