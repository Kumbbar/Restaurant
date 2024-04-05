from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.food.models import Restaurant


class User(AbstractUser):
    current_restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)

