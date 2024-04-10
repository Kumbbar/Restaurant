from rest_framework import serializers
from .models import Dish, DishType, Restaurant, Menu, RestaurantPlanMenu, Client


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
