from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow users to view or edit their own profile,
    or allow administrators (staff) full access.
    """

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        if not (request.user and request.user.is_authenticated):
            return False
        if view.action == 'list':
            return bool(request.user.is_staff)
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user

