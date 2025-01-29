from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    message = 'You are not the owner of the object.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return obj == request.user