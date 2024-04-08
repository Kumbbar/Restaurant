from django.db import models
from django.shortcuts import render, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.validation.query import validate_query_data
from core.views.many_to_many import ManyToManyApiView
from core.views.permissions import LoginRequiredApiView
from .models import Dish, DishType, Restaurant, Menu, RestaurantPlanMenu
from core.viewsets import CoreViewSet
from .serializers import DishSerializer, DishTypeSerializer, RestaurantSerializer, MenuSerializer, \
    RestaurantPlanMenuSerializer


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


class RestaurantPlanMenuViewSet(LoginRequiredApiView, CoreViewSet):
    queryset = RestaurantPlanMenu.objects.all()
    search_fields = ['date_start', 'date_start']
    filterset_fields = ['menu', 'restaurant']
    serializer_class = RestaurantPlanMenuSerializer


class MenuTemplate(APIView):
    def get(self, request, menu_id):
        menu = get_object_or_404(Menu, pk=menu_id)
        dish_types_order = validate_query_data(request.GET.get('order', ''))
        ordered_menu_dishes = self.order_menu_dishes(menu, dish_types_order)
        return render(request, 'food/menu.html', {'ordered_menu_dishes': ordered_menu_dishes})

    def order_menu_dishes(self, menu, dish_types_order):
        result = []
        for dish_type_id in dish_types_order:
            current_dish_type = get_object_or_404(DishType, pk=dish_type_id)
            menu_current_type_dishes = menu.dishes.filter(dish_type=current_dish_type)
            result.append(
                dict(
                    type=current_dish_type,
                    dishes=menu_current_type_dishes
                )
            )
        return result


class Test(APIView):
    def post(self, request):
        menu = Menu.objects.get(pk=1)
        dish = Dish.objects.get(pk=2)
        menu.dishes.add(dish)
        dish = Dish.objects.get(pk=2)
        menu.dishes.add(dish)
        return Response(status=200)
