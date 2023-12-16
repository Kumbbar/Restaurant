from typing import Callable

from django.contrib.auth.validators import UnicodeUsernameValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.users.models import User
from ..services.users import create_user
from ..services.selectors.users import get_all_users
from ..services.passwords import validate_password


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    model = User
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    validate_new_password: Callable = staticmethod(validate_password)


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=6,
        max_length=150,
        validators=[
            UniqueValidator(get_all_users()),
            UnicodeUsernameValidator
        ]
    )
    date_joined = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(write_only=True)

    validate_password = staticmethod(validate_password)

    def create(self, validated_data):
        user = create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'password')