from .. import User


def create_user(**data) -> User:
    return User.objects.create_user(**data)
