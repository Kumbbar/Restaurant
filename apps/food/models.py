import datetime
from typing import NewType
from django.core.validators import MinLengthValidator
from django.db import models


Minute = NewType('Minutes', int)


class Restaurant(models.Model):
    name = models.CharField(max_length=256, null=False)
    boss = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    date_of_open = models.DateField(auto_now_add=True, null=True)


class DishType(models.Model):
    name = models.CharField(max_length=256, null=False)


class Dish(models.Model):
    """
    Dish version for specific menu
    """
    name = models.CharField(max_length=256, null=False, unique=True)
    description = models.CharField(max_length=256, null=True)
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
    datetime_start = models.DateTimeField(null=False)
    datetime_end = models.DateTimeField(null=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class MobilePhoneModel(models.Model):
    """
    Base model for russian
    mobile phone numbers without country code
    """

    phone_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)],
        null=False
    )


class TableReservation(MobilePhoneModel):
    """
    Table reservation
    """
    table_number = models.IntegerField(null=True)
    name = models.CharField(max_length=256, null=False)
    surname = models.CharField(max_length=256, null=False)
    time_of_start = models.DateTimeField(null=False)
    time_of_end = models.DateTimeField(null=True)
    confirmed = models.BooleanField(default=False, null=False)
    has_come = models.BooleanField(default=False, null=False)
    number_of_people = models.IntegerField(null=False)

    DEFAULT_RESERVATION_TIME: Minute = Minute(30)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.time_of_end is None:
            self.time_of_end += datetime.timedelta(minutes=self.__class__.DEFAULT_RESERVATION_TIME)
        return super().save(force_insert, force_update, using, update_fields)


class PhoneBlackList(MobilePhoneModel):
    blocking_event = models.OneToOneField(TableReservation, on_delete=models.SET_NULL, null=True)

