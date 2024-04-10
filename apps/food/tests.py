from django.test import TestCase

# Create your tests here.
import datetime
from typing import NewType
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.db import models

from apps.food.services.validators import validate_phone_number

Minute = NewType('Minutes', int)


class Restaurant(models.Model):
    name = models.CharField(max_length=256, null=False)
    boss = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    date_of_open = models.DateField(null=True)


class DishType(models.Model):
    name = models.CharField(max_length=256, null=False)


class Dish(models.Model):
    """
    Dish version for specific menu
    """
    name = models.CharField(max_length=256, null=False, unique=True)
    description = models.CharField(max_length=5000, null=True)
    dish_type = models.ForeignKey(DishType, on_delete=models.SET_NULL, null=True)
    weight = models.FloatField(null=True)
    price = models.FloatField(null=True)
    image = models.ImageField(null=True, upload_to='images/')


class Menu(models.Model):
    """
    List of dishes for a specific dates
    """
    name = models.CharField(max_length=256, null=False)
    dishes = models.ManyToManyField(Dish)


class RestaurantPlanMenu(models.Model):
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class Client(models.Model):
    name = models.CharField(max_length=256, null=False)
    surname = models.CharField(max_length=256, null=False)
    patronymic = models.CharField(max_length=256, null=True)
    phone_number = models.CharField(
        max_length=30,
        validators=[validate_phone_number],
        null=False,
        unique=True
    )


class TableReservation(models.Model):
    table_number = models.IntegerField(null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    time_of_start = models.DateTimeField(null=False)
    time_of_end = models.DateTimeField(null=True)
    confirmed = models.BooleanField(default=False, null=False)
    has_come = models.BooleanField(default=False, null=False)
    number_of_people = models.IntegerField(null=False, default=1)

    DEFAULT_RESERVATION_TIME: Minute = Minute(30)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.time_of_end is None:
            self.time_of_end += datetime.timedelta(minutes=self.__class__.DEFAULT_RESERVATION_TIME)
        return super().save(force_insert, force_update, using, update_fields)


class OrderStage(models.Model):
    name = models.CharField(max_length=256, null=False)


class OrderDish(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(validators=[MaxValueValidator(100)])
    stage = models.ForeignKey(OrderStage, on_delete=models.SET_DEFAULT, null=False, default=1)


class Order(models.Model):
    dishes = models.ManyToManyField(OrderDish)
    client = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True)


class ClientBlackList(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False)

