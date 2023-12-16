from django.urls import path, include

from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register('users', views.UserViewSet)
router.register('permissions', views.PermissionViewSet)
router.register('content_types', views.ContentTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'users/<int:pk>/reset_password',
        views.ForceResetUserPasswordApiView.as_view(), name='admin_reset_user_password'
    )
]
