from typing import Callable

from django.contrib.auth.models import Permission, ContentType

from rest_framework import serializers

from apps.users.models import User

from core.services.passwords import validate_password


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


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    model = User
    new_password = serializers.CharField(required=True)
    validate_new_password: Callable = staticmethod(validate_password)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'name',
            'content_type',
            'codename'
        )


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = (
            'app_label',
            'model'
        )