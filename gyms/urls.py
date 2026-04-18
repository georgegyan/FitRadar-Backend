from django.urls import path
from .views import GymListCreateView, GymOwnerListView, GymOwnerManageView

urlpatterns = [
    path('', GymListCreateView.as_view(), name='gym-list-create'),
    path('owner/', GymOwnerListView.as_view(), name='gym-owner-list'),
    path('<int:pk>/', GymOwnerManageView.as_view(), name='gym-owner-manage'),
]