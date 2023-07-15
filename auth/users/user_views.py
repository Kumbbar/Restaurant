from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView

from .models import User
from .permissions import UserOwnerPermission
from .serializers import (
    RegisterUserSerializer,
    ResetPasswordSerializer,
)
from .services.tokens import get_or_create_token
from .services.users import reset_user_password
from .services.selectors.users import get_user_by_id
from .base_views import ResetUserPasswordApiView


# User permission views

class UserLoginAPI(ObtainAuthToken):
    permission_classes = (AllowAny, )

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
            'id': user.pk,
            'email': user.email
        }

        return Response(output_data, status=status.HTTP_200_OK)


class UserLogoutAPI(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserRegisterAPI(CreateAPIView):
    model = User
    permission_classes = (AllowAny, )
    serializer_class = RegisterUserSerializer
    
    
class UserSelfDeleteAPI(DestroyAPIView):
    permission_classes = (IsAuthenticated, UserOwnerPermission, )
    model = User

    def get_queryset(self):
        queryset = get_user_by_id(self.request.user.id)
        return queryset


class UserResetPasswordAPI(ResetUserPasswordApiView):
    def get_object(self, queryset=None, *args, **kwargs):
        obj = self.request.user
        return obj

    def reset_password(self, user: User, serializer: Serializer):
        if not user.check_password(serializer.data.get("old_password"),):
            return Response({"password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IsAuthenticatedView(APIView):
    """
    View for microservices auth check.
    User permissions for services.
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        response_data = {
            'is_superuser': request.user.is_superuser,
            'permissions': request.user.get_all_permissions()
        }
        return Response(response_data, status=status.HTTP_200_OK)
