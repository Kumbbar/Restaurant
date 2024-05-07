from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from core.permissions import AdminPermission, FoodPermission, ClientServicePermission, CookingPermission


class PublicApiView:
    authentication_classes = ()
    permission_classes = (AllowAny, )


class AdminApiView:
    permission_classes = (IsAuthenticated, IsAdminUser | AdminPermission)


class FoodApiView:
    permission_classes = (IsAuthenticated, FoodPermission)


class ClientServiceApiView:
    permission_classes = (IsAuthenticated, ClientServicePermission)


class CookingApiView:
    permission_classes = (IsAuthenticated, CookingPermission)


class LoginRequiredApiView:
    permission_classes = (IsAuthenticated,)
