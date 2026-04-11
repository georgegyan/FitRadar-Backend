from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.views import RegisterView, ProfileView, CustomTokenObtainPairView

@api_view(['GET'])
def api_root(request):
    return Response({
        'authentication': {
            'register': '/api/auth/register/',
            'login': '/api/auth/login/',
            'refresh_token': '/api/auth/token/refresh/',
            'profile': '/api/auth/profile/',
        },
        'gyms': {
            'list_nearby': '/api/gyms/?lat=&lng=',
            'detail': '/api/gyms/{id}/',
            'create': '/api/gyms/create/',
            'update': '/api/gyms/{id}/update/',
            'gym_bookings': '/api/gyms/{id}/bookings/',
        },
        'bookings': {
            'my_bookings': '/api/bookings/',
            'create': '/api/bookings/create/',
            'detail': '/api/bookings/{id}/',
            'cancel': '/api/bookings/{id}/cancel/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/profile/', ProfileView.as_view(), name='profile'),
    path('api/gyms/', include('gyms.urls')),
    path('api/bookings/', include('bookings.urls')),
]