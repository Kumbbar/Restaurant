from rest_framework import status
from rest_framework.exceptions import APIException


class BadQueryParams(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid'
