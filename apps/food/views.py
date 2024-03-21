from django.db import models
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.views.many_to_many import ManyToManyApiView
from core.views.permissions import LoginRequiredApiView
from .models import Dish, DishType, Restaurant, Menu
from core.viewsets import CoreViewSet
from .serializers import DishSerializer, DishTypeSerializer, RestaurantSerializer, MenuSerializer


class DishViewSet(LoginRequiredApiView, CoreViewSet):
    queryset = Dish.objects.all()
    search_fields = ['name']
    serializer_class = DishSerializer
    parser_classes = (MultiPartParser, FormParser)


class DishTypeViewSet(LoginRequiredApiView, CoreViewSet):
    queryset = DishType.objects.all()
    search_fields = ['name']
    serializer_class = DishTypeSerializer


class RestaurantViewSet(LoginRequiredApiView, CoreViewSet):
    queryset = Restaurant.objects.all()
    search_fields = ['name']
    serializer_class = RestaurantSerializer


class MenuViewSet(LoginRequiredApiView, CoreViewSet):
    queryset = Menu.objects.all()
    search_fields = ['name']
    serializer_class = MenuSerializer


class ChangeMenuDishesApiView(LoginRequiredApiView, ManyToManyApiView):
    changeable_model = Menu
    serializer = DishSerializer
    many_to_many_field = 'dishes'


class Test(APIView):
    def post(self, request):
        menu = Menu.objects.get(pk=1)
        dish = Dish.objects.get(pk=2)
        menu.dishes.add(dish)
        dish = Dish.objects.get(pk=2)
        menu.dishes.add(dish)
        return Response(status=200)
