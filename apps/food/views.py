from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dish, DishType, Restaurant, Menu
from core.viewsets import CoreViewSet
from .serializers import DishSerializer, DishTypeSerializer, RestaurantSerializer


class DishViewSet(CoreViewSet):
    queryset = Dish.objects.all()
    search_fields = ['name']
    serializer_class = DishSerializer
    parser_classes = (MultiPartParser, FormParser)


class DishTypeViewSet(CoreViewSet):
    queryset = DishType.objects.all()
    search_fields = ['name']
    serializer_class = DishTypeSerializer


class RestaurantViewSet(CoreViewSet):
    queryset = Restaurant.objects.all()
    search_fields = ['name']
    serializer_class = RestaurantSerializer


class Test(APIView):
    def post(self, request):
        menu = Menu.objects.get(pk=1)
        dish = Dish.objects.get(pk=2)
        menu.dishes.add(dish)
        dish = Dish.objects.get(pk=2)
        menu.dishes.add(dish)
        return Response(status=200)
