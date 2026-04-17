from django.urls import path
from .views import GymListCreateView

urlpatterns = [
    path('', GymListCreateView.as_view(), name='gym-list-create'),
]