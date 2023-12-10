from django.contrib.auth.validators import UnicodeUsernameValidator
import django.contrib.auth.password_validation as validators

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..models import User
from ..services.tokens import create_token
from ..serializers import CreateUserSerializer


class RegisterUserSerializer(CreateUserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data):
        user = super().create(validated_data)
        self.token = create_token(user=user)
        return user

    def get_token(self, obj):
        return self.token.key

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'token', 'date_joined', 'password')