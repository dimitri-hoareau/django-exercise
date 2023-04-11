from rest_framework.permissions import BasePermission, SAFE_METHODS

class CreateOnly(BasePermission):
    """
    Custom permission class that allows only POST requests.
    """
    def has_permission(self, request, view):
        return request.method == 'POST'
    
class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission class that allows owners to edit their own sales but only allows
    read-only access to other users.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for all requests, so we'll always allow GET, HEAD, and OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the sale.
        return obj.author == request.user