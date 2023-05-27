from django.urls import path

from . import views as views

urlpatterns = [
    path('register/', views.UserRegisterAPI.as_view(), name='register'),
    path('login/', views.UserLoginAPI.as_view(), name='login'),
    path('logout/', views.UserLogoutAPI.as_view(), name='logout'),
    path('delete_user/<int:pk>', views.UserDeleteAPI.as_view(), name='delete_user'),
]