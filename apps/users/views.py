from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView

from .models import User
from .permissions import UserOwnerPermission
from .serializers import (
    RegisterUserSerializer
)
from core.services.tokens import get_or_create_token
from core.services.selectors.users import get_user_by_id
from core.abc_views.users import ResetUserPasswordApiView
from core.views.permissions import PublicApiView


class UserRegisterAPI(PublicApiView, CreateAPIView):
    model = User
    serializer_class = RegisterUserSerializer


class UserLoginAPI(PublicApiView, ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = get_or_create_token(user)
        output_data = {
            'token': token.key,
            'id': user.pk
        }
        return Response(output_data, status=status.HTTP_200_OK)


class UserLogoutAPI(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserSelfDeleteAPI(DestroyAPIView):
    permission_classes = (IsAuthenticated, UserOwnerPermission, )
    model = User

    def get_object(self):
        object = get_user_by_id(self.request.user.id)
        return object


class UserResetPasswordAPI(ResetUserPasswordApiView):
    def get_object(self, queryset=None, *args, **kwargs):
        obj = self.request.user
        return obj

    def reset_password(self, user: User, serializer: Serializer):
        if not user.check_password(serializer.data.get("password"),):
            return Response({"password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IsAuthenticatedView(APIView):
    """
    User data.
    """
    attrs = (
        'id',
        'first_name',
        'last_name',
        'email',
        'username',
        'is_superuser',
        'is_staff',
        'is_superuser',
    )

    def get(self, request):
        response_data = {attr: getattr(request.user, attr) for attr in self.__class__.attrs}
        response_data['permissions'] = request.user.get_user_permissions()
        return Response(response_data, status=status.HTTP_200_OK)
