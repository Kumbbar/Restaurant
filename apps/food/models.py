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
        null=True,
        unique=True
    )


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False)
    number = models.IntegerField(null=False)
    description = models.CharField(max_length=2000, null=True)


class TableReservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    time_of_start = models.DateTimeField(null=False)
    time_of_end = models.DateTimeField(null=True)
    confirmed = models.BooleanField(default=False, null=False)
    has_come = models.BooleanField(default=None, null=False)
    number_of_people = models.IntegerField(null=False, default=1)

    DEFAULT_RESERVATION_TIME: Minute = Minute(30)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.time_of_end is None:
            self.time_of_end = self.__class__.add_default_reservation_time(self.time_of_start)
        return super().save(force_insert, force_update, using, update_fields)

    @classmethod
    def add_default_reservation_time(cls, time):
        return time + datetime.timedelta(minutes=cls.DEFAULT_RESERVATION_TIME)


class OrderStages:
    NOT_READY = "not ready"
    READY = "ready"
    FINISHED = "finished"

    ORDER_STAGES_CHOICES = (
        (NOT_READY, "not ready"),
        (READY, "ready"),
        (FINISHED, "finished")
    )


class Order(models.Model):
    dishes = models.ManyToManyField(Dish, through='OrderDish')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    stage = models.CharField(null=False,
                             max_length=256,
                             choices=OrderStages.ORDER_STAGES_CHOICES, default=OrderStages.NOT_READY
                             )
    created_at = models.DateTimeField(auto_now_add=True)


class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=False)
    count = models.IntegerField()
    stage = models.CharField(null=False,
                             max_length=256,
                             choices=OrderStages.ORDER_STAGES_CHOICES, default=OrderStages.NOT_READY
                             )


class ClientBlackList(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, null=False)