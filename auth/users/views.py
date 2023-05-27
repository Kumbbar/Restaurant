from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView

from .models import User
from .permissions import UserOwnerPermission
from .serializers import RegisterUserSerializer, UserDeleteOutputSerializer
from .services.tokens import get_or_create_token
from .services.selectors.users import get_all_users


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
    queryset = get_all_users()
    model = User
    serializer_class = UserDeleteOutputSerializer
    

