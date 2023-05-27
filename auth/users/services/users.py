from ..models import User


def create_user(**data):
    return User.objects.create_user(**data)