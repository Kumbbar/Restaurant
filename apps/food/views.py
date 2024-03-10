from rest_framework.parsers import MultiPartParser, FormParser

from .models import Dish, DishType
from core.viewsets import CoreViewSet
from .serializers import DishSerializer, DishTypeSerializer


class DishViewSet(CoreViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    parser_classes = (MultiPartParser, FormParser)


class DishTypeViewSet(CoreViewSet):
    queryset = DishType.objects.all()
    serializer_class = DishTypeSerializer


