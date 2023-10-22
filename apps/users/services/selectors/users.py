from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from ...models import User


def get_all_users() -> QuerySet[User]:
    return User.objects.all()


def get_user_by_id(id: int) -> QuerySet[User]:
    return User.objects.filter(pk=id)
