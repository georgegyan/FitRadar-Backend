from django.urls import path
from .views import GymListCreateView, GymOwnerListView, GymOwnerManageView, GymDetailView

urlpatterns = [
    path('', GymListCreateView.as_view(), name='gym-list-create'),
    path('<int:pk>/', GymDetailView.as_view(), name='gym-detail'),
    path('my-gyms/', GymOwnerListView.as_view(), name='gym-owner-list'),
    path('my-gyms/<int:pk>/', GymOwnerManageView.as_view(), name='gym-owner-manage'),
]