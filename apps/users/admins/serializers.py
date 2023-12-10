from typing import Callable

from rest_framework import serializers

from ..models import User
from ..serializers import CreateUserSerializer
from ..services.passwords import validate_password


class UsersRUDListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
            'is_active',
            'email',
            'date_joined'
        )


class AdminCreateUserSerializer(CreateUserSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
            'is_active',
            'email',
            'date_joined'
        )


class AdminResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    model = User
    new_password = serializers.CharField(required=True)
    validate_new_password: Callable = staticmethod(validate_password)
