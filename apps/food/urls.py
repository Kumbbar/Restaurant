from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register('dishes', views.DishViewSet)
router.register('dish_types', views.DishTypeViewSet)
router.register('restaurants', views.RestaurantViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('test/', views.Test.as_view())
    ]
