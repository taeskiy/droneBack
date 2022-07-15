from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from apps.user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    TYPE_CUSTOMER = 'customer'
    TYPE_CRM_ADMIN = 'crm_admin'

    USER_TYPES = (
        (TYPE_CUSTOMER, 'Клиент'),
        (TYPE_CRM_ADMIN, 'Админ CRM'),
    )
    user_type = models.CharField('Тип пользователя', choices=USER_TYPES, max_length=16, default=TYPE_CUSTOMER)
    phone_number = PhoneNumberField('Телефон', unique=True)
    # country = models.ForeignKey('countries.Country', models.SET_NULL, null=True)
    company_name = models.CharField('Компания', max_length=50, null=True, blank=True)
    first_name = models.CharField('Имя', max_length=50, null=True, blank=True)
    last_name = models.CharField('Фамилия', max_length=50, null=True, blank=True)
    middle_name = models.CharField('Отчество', max_length=50, null=True, blank=True)
    email = models.EmailField('Электронная почта', max_length=255, null=True, blank=True, unique=True)
    avatar = models.ImageField(upload_to='upload/users/avatar', null=True, blank=True)
    gender = models.BooleanField('Пол', null=True)
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    date_of_birth = models.DateTimeField('Дата рождения', null=True)
    updated_date = models.DateTimeField('Дата изменения', auto_now=True)
    is_active = models.BooleanField('Активный', default=False)
    is_staff = models.BooleanField('Админ', default=False)
    notification_token = models.CharField(max_length=255, null=True, blank=True)
    is_notification = models.BooleanField(default=True)

    has_individual_commission = models.BooleanField('Имеет индивидуальный процент', default=False)
    commission_percent = models.PositiveSmallIntegerField('Процент сервиса', default=8,
                                                          validators=[
                                                              MaxValueValidator(100),
                                                              MinValueValidator(0)
                                                          ])

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    balance = models.DecimalField('Баланс', decimal_places=2, max_digits=10, default=0.00)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        return str(self.phone_number)

    def get_short_name(self):
        return str(self.phone_number)

    def __str__(self):
        return self.get_short_name()

    def save(self, *args, **kwargs):
        save = super().save(*args, **kwargs)
        return save

    @property
    def is_crm_admin(self):
        return self.TYPE_CRM_ADMIN == self.user_type
