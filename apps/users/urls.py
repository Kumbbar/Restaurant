from django.urls import path

from . import user_views as views

urlpatterns = [
    path('register/', views.UserRegisterAPI.as_view(), name='register'),
    path('login/', views.UserLoginAPI.as_view(), name='login'),
    path('logout/', views.UserLogoutAPI.as_view(), name='logout'),
    path('delete_me/', views.UserSelfDeleteAPI.as_view(), name='delete_me'),
    path('reset_password/', views.UserResetPasswordAPI.as_view(), name='reset_password'),
    path('is_authenticated/', views.IsAuthenticatedView.as_view(), name='is_authenticated'),
]
