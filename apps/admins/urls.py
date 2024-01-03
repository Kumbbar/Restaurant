from django.urls import path, include

from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register('users', views.UserViewSet)
router.register('permissions', views.PermissionViewSet)
router.register('groups', views.GroupViewSet)
router.register('content_types', views.ContentTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'users/<int:pk>/reset_password',
        views.ForceResetUserPasswordApiView.as_view(), name='admin_reset_user_password'
    ),

    path(
        'group_permissions/<int:main_id>/',
        views.ChangeGroupPermissionsApiView.as_view(), name='change_group_permissions'
    ),
    path(
        'user_groups/<int:main_id>/',
        views.ChangeUserGroupsApiView.as_view(), name='change_user_groups'
    ),
    path(
        'user_permissions/<int:main_id>/',
        views.ChangeUserPermissionsApiView.as_view(), name='change_user_permissions'
    ),
]
