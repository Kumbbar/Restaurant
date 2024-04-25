from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    permission: str

    def has_permission(self, request, view):
        return request.user.has_perm(self.__class__.permission)


class AdminPermission(UserPermission):
    permission = 'food.admin_permission'


class FoodPermission(UserPermission):
    permission = 'food.food_permission'


class ClientServicePermission(UserPermission):
    permission = 'food.client_service_permission'


class CookingPermission(UserPermission):
    permission = 'food.cooking_permission'

