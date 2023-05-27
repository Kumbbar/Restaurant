from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework.validators import UniqueValidator

from .models import User
from .services.users import create_user
from .services.tokens import create_token
from .services.selectors.users import get_all_users


class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=6,
        max_length=150,
        validators=[
            UniqueValidator(get_all_users()),
            UnicodeUsernameValidator
        ]
    )
    token = serializers.SerializerMethodField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = create_user(**validated_data)
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


class UserDeleteOutputSerializer(serializers.ModelSerializer):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'password')


