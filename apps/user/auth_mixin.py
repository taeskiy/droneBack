import datetime
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.decorators import action

from apps.services.exceptions import BadRequest

from rest_framework.response import Response

from apps.user.exceptions import UserDoesntExist, ActivationCodeInvalid
from apps.user.models import User, ActivateCode, UserFCMTokens
from apps.user.serializers import PhoneSerializer, CodeSeriliazer, UserSerializer, ShortUserSerializer, \
    UserRegisterSerializer, UserPasswordSerializer, GetTokenSerializer, UserLogOutSerializer, \
    UserChangePasswordSerializer
from apps.utils import random_with_N_digits
from ataba.settings import DEBUG
from custom_jwt.utils import get_token
from nikita_sms.sender import send_sms


class SMSAuthMixin:
    @swagger_auto_schema(method='post',
                         operation_description="POST /register/",
                         request_body=UserRegisterSerializer,
                         responses={201: UserRegisterSerializer})
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = True
        user.save()
        random_code = 7777
        now = datetime.datetime.now()
        valid_till = now + datetime.timedelta(seconds=ActivateCode.VALID_TILL_SECONDS)
        code, created = ActivateCode.objects.get_or_create(user=user, defaults={'user': user, 'value': random_code,
                                                                         'valid_till': valid_till})
        if not created:
            code.value = random_code
            code.valid_till = valid_till
            code.save()
        history_id = int(now.timestamp())
        if not DEBUG:
            send_sms(history_id, str(random_code), [user.phone_number])
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(method='post',
                         operation_description="POST /send-code/",
                         request_body=PhoneSerializer,
                         responses={201: ''})
    @action(detail=False, methods=['post'])
    def send_code(self, request):
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise UserDoesntExist
        if phone_number in ['+996772177987', '+996705073377', '+996500369152', '+996773288644']:
            random_code = 7777
        else:
            random_code = random_with_N_digits(4)
        # TODO: REMOVE FOR PRODUCTION
        # random_code = 7777
        now = datetime.datetime.now()
        valid_till = now + datetime.timedelta(seconds=ActivateCode.VALID_TILL_SECONDS)
        code, created = ActivateCode.objects.get_or_create(user=user, defaults={'user': user, 'value': random_code,
                                                                                'valid_till': valid_till})

        if not created:
            code.value = random_code
            code.valid_till = valid_till
            code.save()
        history_id = int(now.timestamp())
        if phone_number not in ['+996772177987', '+996705073377', '+996500369152', '+996773288644']:
            send_sms(history_id, str(random_code), [phone_number])
        return Response(str(random_code), status=status.HTTP_201_CREATED)

    @swagger_auto_schema(method='post',
                         operation_description="POST /get-token/",
                         request_body=CodeSeriliazer,
                         responses={200: GetTokenSerializer})
    @action(detail=False, methods=['post'])
    def get_token(self, request):
        serializer = CodeSeriliazer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        phone_number = serializer.validated_data['phone_number']

        try:
            user = User.objects.get(phone_number=phone_number)
        except ObjectDoesNotExist:
            raise BadRequest('Пользователя с таким номером не существует')

        now = datetime.datetime.now().replace(tzinfo=None)
        try:
            if user.activate_code.valid_till.replace(tzinfo=None) <= now:
                raise ActivationCodeInvalid
            if serializer.validated_data.get('notification_token', None):
                user.notification_token = serializer.validated_data['notification_token']

            if user.activate_code.value == code:
                user.is_active = True
                user.save()
                return Response({"token": get_token(user), "user": ShortUserSerializer(user, context={'request': request}).data})
        except:
            raise
            pass
        raise ActivationCodeInvalid

    @swagger_auto_schema(method='post',
                         operation_description="POST /register/",
                         request_body=UserPasswordSerializer,
                         responses={201: ''})
    @action(detail=False, methods=['post'],
            permission_classes=[permissions.IsAuthenticated])
    def reset_password(self, request):
        serializer = UserPasswordSerializer(instance=request.user,
                                            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(method='post',
                         request_body=UserLogOutSerializer)
    @action(detail=False, methods=['post'],
            permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        serializer = UserLogOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            if request.data.get('firebase_token', None):
                if serializer.validated_data['is_ios']:
                    UserFCMTokens.objects.get(
                        user=request.user,
                        apns_token=serializer.validated_data['firebase_token']
                    ).delete()
                else:
                    UserFCMTokens.objects.get(
                        user=request.user,
                        firebase_token=serializer.validated_data['firebase_token']
                    ).delete()
        except:
            pass
        return Response({"status": "ok"})

    @swagger_auto_schema(method='post',
                         request_body=UserChangePasswordSerializer,
                         responses={200: ''})
    @action(detail=False, methods=['post'],
            permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        serializer = UserChangePasswordSerializer(instance=request.user,
                                            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_200_OK
        )
