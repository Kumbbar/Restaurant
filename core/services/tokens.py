from rest_framework.authtoken.models import Token

from .. import User


def get_or_create_token(user: User) -> Token:
    return Token.objects.get_or_create(user=user)


def create_token(user: User) -> Token:
    return Token.objects.create(user=user)
