from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .serializers import (
    UsersRUDListSerializer,
    ResetPasswordSerializer,
    PermissionSerializer,
    ContentTypeSerializer
)
from .services.selectors.permissions import get_all_permissions
from .services.selectors.content_types import get_all_content_types
from apps.users.models import User

from core.services.selectors.users import get_all_users, get_user_by_id
from core.abc_views.users import ResetUserPasswordApiView
from core.views.permissions import AdminApiView
from core.serializers.users import CreateUserSerializer
from core.viewsets import CoreViewSet


class UserViewSet(CoreViewSet, AdminApiView):
    queryset = get_all_users()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        else:
            return UsersRUDListSerializer


class PermissionViewSet(CoreViewSet, AdminApiView):
    queryset = get_all_permissions()
    serializer_class = PermissionSerializer

    search_fields = ['codename', 'name']
    filterset_fields = ['content_type_id']
    ordering_fields = ['codename']
    ordering = ['-codename']


class ContentTypeViewSet(CoreViewSet, AdminApiView):
    queryset = get_all_content_types()
    serializer_class = ContentTypeSerializer

    search_fields = ['app_label', 'model']
    ordering_fields = ['app_label']
    ordering = ['-app_label']


class ForceResetUserPasswordApiView(AdminApiView, ResetUserPasswordApiView):
    serializer_class = ResetPasswordSerializer

    def get_object(self, queryset=None, *args, **kwargs):
        obj = get_user_by_id(kwargs['pk']).first()
        return obj

    def reset_password(self, user: User, serializer: Serializer):
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)