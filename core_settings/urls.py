from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import settings
from .settings import DEBUG


urlpatterns = [
    path('auth/', include('apps.users.urls')),
    path('admin/', include('apps.admins.urls')),
    path('food/', include('apps.food.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
4
debug_urls = (
    path('docs/', include('rest_framework.urls')),
    path('admin_panel/', admin.site.urls)
)

if DEBUG:
    urlpatterns.extend(debug_urls)

