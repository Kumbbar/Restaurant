from rest_framework import serializers
from .models import Dish, DishType, Restaurant, Menu, RestaurantPlanMenu, Client, Table, Order, OrderDish


class DishSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
            'description',
            'dish_type',
            'weight',
            'price',
            'image'
        )


class DishTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishType
        fields = (
            'id',
            'name'
        )


class RestaurantSerializer(serializers.ModelSerializer):
    date_of_open = serializers.DateField(required=False)

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'boss',
            'latitude',
            'longitude',
            'date_of_open'
        )


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            'id',
            'name'
        )


class RestaurantPlanMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantPlanMenu
        fields = ('id', 'menu', 'restaurant', 'date_start', 'date_end')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name', 'surname', 'patronymic', 'phone_number')


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = (
            'id',
            'restaurant',
            'number',
            'description'
        )


class OrderDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDish
        fields = (
            'id',
            'dish',
            'order',
            'count',
            'stage'
        )


class OrderDishCookSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(source='order.created_at')
    table = serializers.IntegerField(source='order.table.number', allow_null=True)

    class Meta:
        model = OrderDish
        fields = (
            'id',
            'dish',
            'count',
            'table',
            'created_at'
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'client',
            'table',
            'stage',
            'created_at'
        )
        read_only_fields = ['created_at', 'stage']


