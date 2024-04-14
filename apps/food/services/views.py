import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from apps.food.models import OrderDish, OrderStages
from apps.food.serializers import OrderDishCookSerializer
from core.views.permissions import LoginRequiredApiView
from core.viewsets import CoreGetUpdateOnlyViewSet


class BaseOrderDishEditViewSet(LoginRequiredApiView, CoreGetUpdateOnlyViewSet):
    search_fields = ['dish__name', 'order__client__surname', 'order__table__number']
    serializer_class = OrderDishCookSerializer
    stage_to_set: str
    stage_to_search: str

    def get_queryset(self):
        ordered_dishes = OrderDish.objects.filter(
            order__restaurant=self.request.user.current_restaurant,
            order__created_at__lte=datetime.datetime.now(),
            stage=self.__class__.stage_to_search
        ).order_by('-id')
        return ordered_dishes

    def update(self, request, *args, **kwargs):
        order_dish = get_object_or_404(OrderDish, pk=kwargs['pk'])
        order_dish.stage = self.__class__.stage_to_set
        order_dish.save()
        all_order_dishes = OrderDish.objects.filter(order=order_dish.order)
        dishes_ready = [order_dish.stage == self.__class__.stage_to_set for order_dish in all_order_dishes]
        if all(dishes_ready):
            order_dish.order.stage = self.__class__.stage_to_set
            order_dish.order.save()
        return Response(status=status.HTTP_200_OK)