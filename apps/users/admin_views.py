from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import User
from .serializers import (
    AdminCreateUserSerializer,
    UsersRUDListSerializer, AdminResetPasswordSerializer
)
from .services.selectors.users import get_all_users, get_user_by_id
from .base_views import ResetUserPasswordApiView


class UserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = get_all_users()
    serializer_class = UsersRUDListSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return AdminCreateUserSerializer
        else:
            return UsersRUDListSerializer


class AdminResetUserPasswordApiView(ResetUserPasswordApiView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = AdminResetPasswordSerializer

    def get_object(self, queryset=None, *args, **kwargs):
        obj = get_user_by_id(kwargs['pk']).first()
        return obj

    def reset_password(self, user: User, serializer: Serializer):
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
