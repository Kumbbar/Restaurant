from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from .serializers import (
    UsersRUDListSerializer,
    ResetPasswordSerializer,
    PermissionSerializer,
    ContentTypeSerializer,
    GroupSerializer
)
from .services.selectors.permissions import get_all_permissions
from .services.selectors.content_types import get_all_content_types
from .services.selectors.groups import get_all_groups
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


class GroupViewSet(CoreViewSet, AdminApiView):
    queryset = get_all_groups()
    serializer_class = GroupSerializer

    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['-name']


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


class TestApi(APIView):
    model_main_id_field = 'pk'
    model_optional_id_field = 'pk'
    model = None

    def get(self, request, main_id, optional_id=None):

        data = PermissionSerializer(Group.objects.get(pk=main_id).permissions.all(), many=True)

        return Response(data=data.data, status=status.HTTP_204_NO_CONTENT)
