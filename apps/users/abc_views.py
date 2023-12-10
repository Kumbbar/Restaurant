from abc import ABC, abstractmethod

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework.serializers import Serializer

from .models import User
from .serializers import (
    ResetPasswordSerializer
)


class ResetUserPasswordApiView(ABC, UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    @abstractmethod
    def get_object(self, queryset=None, *args, **kwargs):
        pass

    @abstractmethod
    def reset_password(self, user: User, serializer: Serializer):
        pass

    def update(self, request, *args, **kwargs):
        self.object = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = self.reset_password(
                user=self.object,
                serializer=serializer
            )
            return result
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)