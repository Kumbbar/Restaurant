from django.contrib.auth.models import Group
from django.db.models import QuerySet


def get_all_groups() -> QuerySet[Group]:
    return Group.objects.all()
