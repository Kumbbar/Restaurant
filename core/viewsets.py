from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import OrderingFilter, SearchFilter

from core.pagination import CorePagination


class CoreFilterMixin:
    pagination_class = CorePagination
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]

    search_fields = ['id']
    filterset_fields = []

    ordering_fields = ['id']
    ordering = ['-id']


class CoreViewSet(CoreFilterMixin, ModelViewSet):
    pass


class CoreGetOnlyViewSet(CoreFilterMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    pass


class CoreGetUpdateOnlyViewSet(CoreFilterMixin,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.ListModelMixin,
                               GenericViewSet):
    pass
