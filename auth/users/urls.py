from django.urls import path
from . import views as views

urlpatterns = [
    path('register/', views.UserRegisterAPI.as_view()),
    path('login/', views.UserLoginAPI.as_view()),
    path('logout/', views.UserLogoutAPI.as_view()),
    path('delete_user/<int:pk>', views.UserDeleteAPI.as_view()),
]