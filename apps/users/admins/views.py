from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from apps.users.models import User
from apps.users.admins.serializers import (
    AdminCreateUserSerializer,
    UsersRUDListSerializer, AdminResetPasswordSerializer
)
from apps.users.services.selectors.users import get_all_users, get_user_by_id
from apps.users.abc_views import ResetUserPasswordApiView, AdminApiView


class UserViewSet(AdminApiView, ModelViewSet):
    queryset = get_all_users()

    def get_serializer_class(self):
        if self.action == 'create':
            return AdminCreateUserSerializer
        else:
            return UsersRUDListSerializer


class AdminResetUserPasswordApiView(AdminApiView, ResetUserPasswordApiView):
    serializer_class = AdminResetPasswordSerializer

    def get_object(self, queryset=None, *args, **kwargs):
        obj = get_user_by_id(kwargs['pk']).first()
        return obj

    def reset_password(self, user: User, serializer: Serializer):
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
