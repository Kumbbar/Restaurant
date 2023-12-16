from django.urls import path, include

from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'users/<int:pk>/reset_password',
        views.AdminResetUserPasswordApiView.as_view(), name='admin_reset_user_password'
    )
]
