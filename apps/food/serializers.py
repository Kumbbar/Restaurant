from rest_framework import serializers
from .models import Dish, DishType


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
