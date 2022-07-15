from rest_framework.exceptions import APIException


class droneApiException(APIException):
    status_code = 400
