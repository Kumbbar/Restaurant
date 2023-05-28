from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView

from .models import User
from .permissions import UserOwnerPermission
from .serializers import RegisterUserSerializer, ResetPasswordSerializer
from .services.tokens import get_or_create_token
from .services.users import reset_user_password
from .services.selectors.users import get_user_by_id


class UserLoginAPI(ObtainAuthToken):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
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
    permission_classes = [
        AllowAny
    ]
    serializer_class = RegisterUserSerializer
    
    
class UserDeleteAPI(DestroyAPIView):
    permission_classes = (IsAdminUser | UserOwnerPermission, )
    model = User

    def get_queryset(self):
        queryset = get_user_by_id(self.kwargs.get('pk'))
        return queryset


class UserResetPasswordAPI(UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = reset_user_password(
                self.object,
                serializer.data.get("old_password"),
                serializer.data.get("new_password")
            )
            return result
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
