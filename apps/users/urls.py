from django.urls import path, include


urlpatterns = [
    path('auth/', include('apps.users.users.urls')),
    path('admin/', include('apps.users.admins.urls'))
]
