from django.contrib.auth.models import Permission
from django.db.models import QuerySet


def get_all_permissions() -> QuerySet[Permission]:
    return Permission.objects.all()
