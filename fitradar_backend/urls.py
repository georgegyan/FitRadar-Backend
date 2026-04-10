from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import RegisterView, ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    # path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/profile/', ProfileView.as_view(), name='profile'),
    
    # Gyms endpoints
    path('api/gyms/nearby/', include('gyms.urls')),  # Will use nested include
    path('api/gyms/', include('gyms.urls')),
    
    # Bookings endpoints
    path('api/bookings/', include('bookings.urls')),
]