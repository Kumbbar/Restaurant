from rest_framework import serializers
from .models import Dish


class DishSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Dish
        fields = (
            'name',
            'description',
            'menu',
            'dish_type',
            'weight',
            'price',
            'image'
        )

