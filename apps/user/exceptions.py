from rest_framework.exceptions import APIException


class UserDoesntExist(APIException):
    status_code = 404
    default_detail = 'Пользователь с таким телефоном не существует.'
    default_code = 'user_not_found'


class ActivationCodeRequired(APIException):
    status_code = 400
    default_detail = 'Код активации обязателен.'
    default_code = 'activation_code_required'


class ActivationCodeInvalid(APIException):
    status_code = 400
    default_detail = 'Неверный код активации'
    default_code = 'activation_code_invalid'


class PhoneNumberRequired(APIException):
    status_code = 400
    default_detail = 'Номер телефона обязателен.'
    default_code = 'phone_number_required'


class UnexpectedError(APIException):
    status_code = 503
    default_detail = 'Произошла ошибка, обратитесь к администраторам.'
    default_code = 'service_unavailable'


class AlreadyVotedException(APIException):
    status_code = 403
    default_detail = 'Пользователь уже голосовал.'
    default_code = 'already_voted'


class CoordinatesException(APIException):
    status_code = 403
    default_detail = 'Долгота и Широта обязательны.'
    default_code = 'coordinates_empty'


class FirebaseTokenRequired(APIException):
    status_code = 503
    default_detail = 'firebase_token не был предоставлен'
    default_code = 'service_unavailable'
