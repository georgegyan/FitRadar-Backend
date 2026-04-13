from rest_framework import permissions

class IsGymOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow GET requests for everyone (list view)
        if request.method == 'GET':
            return True
        # For POST/PUT/DELETE, require authenticated gym owner
        return request.user and request.user.is_authenticated and request.user.is_gym_owner