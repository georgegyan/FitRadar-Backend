from rest_framework import permissions

class IsBookingOwner(permissions.BasePermission):
    """
    Custom permission to only allow the user who made the booking to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user