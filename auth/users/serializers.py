from django.contrib.auth.validators import UnicodeUsernameValidator
import django.contrib.auth.password_validation as validators

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User
from .services.users import create_user
from .services.tokens import create_token
from .services.selectors.users import get_all_users


# Base serializers

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

    def create(self, validated_data):
        user = create_user(**validated_data)
        return user

    @staticmethod
    def validate_password(password):
        validators.validate_password(password=password)
        return password

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'password')


class RegisterUserSerializer(CreateUserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data):
        user = super().create(validated_data)
        self.token = create_token(user=user)
        return user

    def get_token(self, obj):
        return self.token.key

    @staticmethod
    def validate_password(password):
        validators.validate_password(password=password)
        return password

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'token', 'date_joined', 'password')


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    model = User
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    @staticmethod
    def validate_new_password(password):
        validators.validate_password(password)
        return password


class AdminResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    model = User
    new_password = serializers.CharField(required=True)

    @staticmethod
    def validate_new_password(password):
        validators.validate_password(password)
        return password


# Admin serializers
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
