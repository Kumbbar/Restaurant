from rest_framework import status
from rest_framework.response import Response

from ..models import User


def create_user(**data):
    return User.objects.create_user(**data)


def reset_user_password(user: User, password: str, new_password: str):
    if not user.check_password(password):
        return Response({"password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
