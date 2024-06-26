from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register('dishes', views.DishViewSet)
router.register('planned_dishes', views.MenuPlanDishesViewSet, basename='planned_dishes')
router.register('dish_types', views.DishTypeViewSet)
router.register('restaurants', views.RestaurantViewSet)
router.register('menu', views.MenuViewSet)
router.register('restaurant_plan_menu', views.RestaurantPlanMenuViewSet)
router.register('clients', views.ClientViewSet)
router.register('clients_black_list', views.ClientBlackListViewSet)
router.register('tables', views.TableViewSet)
router.register('table_reservation', views.TableReservationViewSet, basename='table_reservation')
router.register('restaurant_tables', views.RestaurantTablesViewSet, basename='restaurant_tables')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('order_dishes_cook', views.OrderDishCookViewSet, basename='order_dishes_cook')
router.register('order_dishes_ready', views.OrderDishReadyViewSet, basename='order_dishes_ready')


urlpatterns = [
    path('', include(router.urls)),
    path('render_menu/<int:menu_id>/', views.MenuTemplateView.as_view()),
    path('order_price/<int:order_id>/', views.OrderPriceView.as_view()),
    path('order_price_template/<int:order_id>/', views.OrderPriceTemplateView.as_view()),
    path(
        'menu_dishes/<int:main_id>/',
        views.ChangeMenuDishesApiView.as_view(), name='change_menu_dishes'
    ),
    path(
        'order_dishes/<int:order_id>/',
        views.ChangeOrderDishView.as_view(),
        name='change_order_dishes'
    ),
    path('today_restaurant_info/', views.TodayRestaurantInfo.as_view()),
    path('restaurant_report/', views.RestaurantReportView.as_view()),

]
