from django.contrib import admin
from django.urls import path, include

from .settings import DEBUG


urlpatterns = [
    path('auth/', include('apps.users.urls'))
]

debug_urls = (
    path('login/', include('rest_framework.urls')),
    path('admin_panel/', admin.site.urls)
)

if DEBUG:
    urlpatterns.extend(debug_urls)

