from django.contrib.auth.models import ContentType
from django.db.models import QuerySet


def get_all_content_types() -> QuerySet[ContentType]:
    return ContentType.objects.all()
