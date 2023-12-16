from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter

from core.pagination import CorePagination


class CoreViewSet(ModelViewSet):
    pagination_class = CorePagination
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]

    search_fields = ['id']
    filterset_fields = []

    ordering_fields = ['id']
    ordering = ['-id']