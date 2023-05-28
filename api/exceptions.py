from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidTransaction(APIException):
    """Exception raised on invalid transactions"""
    status_code = status.HTTP_403_FORBIDDEN
