from django.urls import path, include


urlpatterns = [
    path('', include('apps.users.users.urls')),
    path('admin/', include('apps.users.admins.urls'))
]
