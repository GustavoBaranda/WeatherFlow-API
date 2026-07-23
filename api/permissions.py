from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow users to view or edit their own profile,
    unless they are administrators (staff).
    """

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user
