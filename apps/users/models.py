from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

from rest_framework.authtoken.models import Token