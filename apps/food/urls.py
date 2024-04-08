from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register('dishes', views.DishViewSet)
router.register('dish_types', views.DishTypeViewSet)
router.register('restaurants', views.RestaurantViewSet)
router.register('menu', views.MenuViewSet)
router.register('restaurant_plan_menu', views.RestaurantPlanMenuViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('test/', views.Test.as_view()),
    path('render_menu/<int:menu_id>/', views.MenuTemplate.as_view()),
    path(
        'menu_dishes/<int:main_id>/',
        views.ChangeMenuDishesApiView.as_view(), name='change_menu_dishes'
    ),
    ]
