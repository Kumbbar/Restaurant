from rest_framework.parsers import MultiPartParser, FormParser

from .models import Dish, DishType, Restaurant
from core.viewsets import CoreViewSet
from .serializers import DishSerializer, DishTypeSerializer, RestaurantSerializer


class DishViewSet(CoreViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    parser_classes = (MultiPartParser, FormParser)


class DishTypeViewSet(CoreViewSet):
    queryset = DishType.objects.all()
    serializer_class = DishTypeSerializer


class RestaurantViewSet(CoreViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


