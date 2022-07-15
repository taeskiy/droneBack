from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    custom_response = {'status_code': None, 'message': None, 'errors': {}}
    if response is not None:
        print(response.data)

        if 'detail' in response.data:
            if response.data['detail'] and isinstance(response.data['detail'], str):
                custom_response['message'] = response.data['detail']
            else:
                custom_response['message'] = 'Произошла ошибка. Пожалуйста обратитесь ' \
                                                                     'администраторам '
        else:
            custom_response['errors'] = response.data
            if isinstance(response.data, list):
                custom_response['message'] = 'Произошла ошибка. Пожалуйста обратитесь ' \
                                             'администраторам'
            else:
                for key, value in response.data.items():
                    message = ''
                    if key != 'non_field_errors':
                        if isinstance(value, str):
                            message = value
                        elif isinstance(value, list):
                            message = value[0]
                        elif isinstance(value, dict):
                            message = "error"
                    else:
                        message = value[0] if isinstance(value, str) is False else value
                    if message and isinstance(message, str):
                        custom_response['message'] = message
                    else:
                        custom_response['message'] = 'Произошла ошибка. Пожалуйста обратитесь ' \
                                                                         'администраторам '
        custom_response['status_code'] = response.status_code
        response.data = custom_response
    return response
