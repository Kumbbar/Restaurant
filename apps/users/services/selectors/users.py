from django.db.models import QuerySet

from ...models import User


def get_all_users() -> QuerySet[User]:
    return User.objects.all()


def get_user_by_id(id: int) -> QuerySet[User]:
    return User.objects.filter(pk=id)
