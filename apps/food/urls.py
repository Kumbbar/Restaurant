from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register('dishes', views.DishViewSet)


urlpatterns = [
    path('', include(router.urls)),
    ]
