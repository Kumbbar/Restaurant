from ..models import User
from rest_framework.authtoken.models import Token


def get_or_create_token(user: User):
    return Token.objects.get_or_create(user=user)


def create_token(user: User):
    return Token.objects.create(user=user)
