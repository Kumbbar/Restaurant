import datetime

from django.db import models
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from openpyxl import Workbook

from core.permissions import ClientServicePermission, CookingPermission, FoodPermission, AdminPermission
from core.validation.query import validate_query_data
from core.views.many_to_many import ManyToManyApiView
from core.views.permissions import LoginRequiredApiView, FoodApiView, ClientServiceApiView, CookingApiView
from .models import Dish, DishType, Restaurant, Menu, RestaurantPlanMenu, Client, Table, Order, OrderDish, OrderStages, \
    TableReservation, ClientBlackList
from core.viewsets import CoreViewSet, CoreGetOnlyViewSet
from .serializers import DishSerializer, DishTypeSerializer, RestaurantSerializer, MenuSerializer, \
    RestaurantPlanMenuSerializer, ClientSerializer, TableSerializer, OrderSerializer, OrderDishSerializer, \
    OrderDishCookSerializer, TableReservationSerializer, ClientBlackListSerializer
from .services.black_list import check_user_is_blocked
from .services.report import get_restaurant_excel_report
from .services.reservation import validate_reservation_time
from .services.views import BaseOrderDishEditViewSet

# Register filters
from .filters import *


class DishViewSet(FoodApiView, CoreViewSet):
    queryset = Dish.objects.all()
    search_fields = ['name']
    serializer_class = DishSerializer
    parser_classes = (MultiPartParser, FormParser)


class MenuPlanDishesViewSet(CoreGetOnlyViewSet):
    permission_classes = (IsAuthenticated, CookingPermission | ClientServicePermission)

    def get_queryset(self):
        result = None

        planned_menus = RestaurantPlanMenu.objects.filter(
            Q(date_end__gte=str(datetime.date.today())) | Q(date_end__isnull=True),
            restaurant=self.request.user.current_restaurant,
            date_start__lte=str(datetime.date.today()),
        )
        for planned_obj in planned_menus:
            if not result:
                result = planned_obj.menu.dishes.all()
            else:
                result = result | planned_obj.menu.dishes.all()

        return result.distinct() if result else RestaurantPlanMenu.objects.none()

    serializer_class = DishSerializer


class DishTypeViewSet(FoodApiView, CoreViewSet):
    queryset = DishType.objects.all()
    search_fields = ['name']
    serializer_class = DishTypeSerializer


class RestaurantViewSet(FoodApiView, CoreViewSet):
    permission_classes = (IsAuthenticated, FoodPermission | AdminPermission)
    queryset = Restaurant.objects.all()
    search_fields = ['name']
    serializer_class = RestaurantSerializer


class MenuViewSet(FoodApiView, CoreViewSet):
    queryset = Menu.objects.all()
    search_fields = ['name']
    serializer_class = MenuSerializer


class ChangeMenuDishesApiView(FoodApiView, ManyToManyApiView):
    changeable_model = Menu
    serializer = DishSerializer
    many_to_many_field = 'dishes'


class RestaurantPlanMenuViewSet(FoodApiView, CoreViewSet):
    queryset = RestaurantPlanMenu.objects.all()
    search_fields = ['restaurant__name', 'menu__name', 'date_start', 'date_start']
    filterset_fields = ['menu', 'restaurant']
    serializer_class = RestaurantPlanMenuSerializer


class ClientViewSet(ClientServiceApiView, CoreViewSet):
    queryset = Client.objects.all()
    search_fields = ['name', 'surname', 'patronymic', 'phone_number']
    serializer_class = ClientSerializer


class ClientBlackListViewSet(ClientServiceApiView, CoreViewSet):
    queryset = ClientBlackList.objects.all()
    search_fields = ['client__name', 'client__surname', 'client__patronymic', 'client__phone_number']
    serializer_class = ClientBlackListSerializer


class TableViewSet(FoodApiView, CoreViewSet):
    queryset = Table.objects.all()
    search_fields = ['restaurant__name', 'number', 'description']
    serializer_class = TableSerializer


class RestaurantTablesViewSet(CoreGetOnlyViewSet):
    ordering = ['-number']
    permission_classes = (IsAuthenticated, CookingPermission | ClientServicePermission)

    def get_queryset(self):
        return Table.objects.filter(restaurant=self.request.user.current_restaurant)

    serializer_class = TableSerializer


class OrderViewSet(ClientServiceApiView, CoreViewSet):
    def get_queryset(self):
        return Order.objects.filter(restaurant=self.request.user.current_restaurant).order_by('-created_at')

    search_fields = ['client__name', 'client__surname', 'table__number']
    serializer_class = OrderSerializer
    filterset_fields = ['stage']

    def perform_create(self, serializer):
        check_user_is_blocked(self.request)
        serializer.save(restaurant=self.request.user.current_restaurant)
        super().perform_create(serializer)

    def perform_update(self, serializer):
        check_user_is_blocked(self.request)
        if serializer.instance.stage != serializer.validated_data['stage']:
            OrderDish.objects.filter(order=serializer.instance).update(stage=serializer.validated_data['stage'])
        super().perform_update(serializer)


class MenuTemplateView(FoodApiView, APIView):
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


class OrderPriceView(ClientServiceApiView, APIView):
    def get_prices(self, order_id):
        result = {}
        order = get_object_or_404(Order, pk=order_id)
        order_dishes = OrderDish.objects.filter(order=order).order_by('id').select_related('dish')

        result_price = 0
        order_dishes_info = []
        for order_dish in order_dishes:
            result_price += order_dish.dish.price * order_dish.count
            order_dish_info = {}
            order_dish_info['name'] = order_dish.dish.name
            order_dish_info['price'] = order_dish.dish.price
            order_dish_info['count'] = order_dish.count
            order_dish_info['total_price'] = order_dish.count * order_dish.dish.price
            order_dishes_info.append(order_dish_info)

        result['result_price'] = result_price
        result['order_dishes_info'] = order_dishes_info
        return result

    def get(self, request, order_id):
        prices = self.get_prices(order_id)
        return Response(data=dict(price=prices['result_price']), status=status.HTTP_200_OK)


class OrderPriceTemplateView(OrderPriceView):
    def get(self, request, order_id):
        prices = self.get_prices(order_id)
        order = get_object_or_404(Order, pk=order_id)
        return render(
            request,
            'food/order_price.html',
            {'prices': prices, 'order': order})


class RestaurantReportView(FoodApiView, APIView):
    def get(self, request):
        return get_restaurant_excel_report(request)


class ChangeOrderDishView(ClientServiceApiView, APIView):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order_dishes = OrderDish.objects.filter(order=order, dish__name__icontains=request.GET['search'])
        serialized_dishes = OrderDishSerializer(data=order_dishes, many=True)
        serialized_dishes.is_valid()
        result = dict(
            count=len(serialized_dishes.data),
            results=serialized_dishes.data
        )
        return Response(data=result, status=status.HTTP_200_OK)

    def create_request_is_invalid(self):
        for key in ['dish_id', 'count']:
            if key not in self.request.data:
                return Response(
                    data=dict(
                        key='must be set'
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )
        if not self.request.data['count'].isdigit():
            return Response(
                data=dict(
                    count='invalid number'
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, order_id):
        error = self.create_request_is_invalid()
        if error:
            return error
        dish_id = int(request.data['dish_id'])
        count = int(request.data['count'])
        order = get_object_or_404(Order, pk=order_id)
        add_dish = get_object_or_404(Dish, pk=dish_id)
        OrderDish.objects.create(order=order, dish=add_dish, count=count)
        order.stage = OrderStages.NOT_READY
        order.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, order_id):
        order_dish_id = request.data.get('order_dish_id', 0)
        get_object_or_404(OrderDish, pk=order_dish_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderDishCookViewSet(CookingApiView, BaseOrderDishEditViewSet):
    stage_to_set = OrderStages.READY
    stage_to_search = OrderStages.NOT_READY


class OrderDishReadyViewSet(ClientServiceApiView, BaseOrderDishEditViewSet):
    stage_to_set = OrderStages.FINISHED
    stage_to_search = OrderStages.READY


class TableReservationViewSet(ClientServiceApiView, CoreViewSet):
    search_fields = ['client__name', 'client__surname', 'table__number', 'time_of_start', 'time_of_end']
    serializer_class = TableReservationSerializer
    ordering = ['-time_of_start']

    def get_queryset(self):
        return TableReservation.objects.filter(restaurant=self.request.user.current_restaurant)

    def perform_create(self, serializer):
        check_user_is_blocked(self.request)
        validate_reservation_time(self.request)
        serializer.save(restaurant=self.request.user.current_restaurant)
        super().perform_create(serializer)

    def perform_update(self, serializer):
        check_user_is_blocked(self.request)
        validate_reservation_time(self.request)
        super().perform_update(serializer)


class TodayRestaurantInfo(LoginRequiredApiView, APIView):
    def get(self, request):
        if not request.user.current_restaurant:
            raise ValidationError(
                {'restaurant': 'your administrator must attach you to restaurant for to get today data'}
            )

        tables_reserved = TableReservation.objects.filter(
            restaurant=request.user.current_restaurant, time_of_start__date=datetime.date.today(),
            time_of_start__gte=datetime.datetime.now()
        ).count()

        not_ready_orders = Order.objects.filter(
            Q(stage=OrderStages.NOT_READY) | Q(stage=OrderStages.READY),
            restaurant=request.user.current_restaurant, created_at__date=datetime.date.today()
        ).count()

        return Response(
            data=dict(tables_reserved=tables_reserved, not_ready_orders=not_ready_orders, ),
            status=status.HTTP_200_OK
        )
