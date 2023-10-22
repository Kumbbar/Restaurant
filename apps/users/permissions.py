from rest_framework import permissions


class UserOwnerPermission(permissions.BasePermission):
    """
    Permission allow to interact user with only his own profile
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user