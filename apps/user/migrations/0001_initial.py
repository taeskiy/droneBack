# Generated by Django 3.2.2 on 2021-09-29 07:03

import apps.user.managers
import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Телефон')),
                ('company_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Компания')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='Электронная почта')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='upload/users/avatar')),
                ('gender', models.BooleanField(null=True, verbose_name='Пол')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_of_birth', models.DateTimeField(null=True, verbose_name='Дата рождения')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активный')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Админ')),
                ('notification_token', models.CharField(blank=True, max_length=255, null=True)),
                ('is_notification', models.BooleanField(default=True)),
                ('has_individual_commission', models.BooleanField(default=False, verbose_name='Имеет индивидуальный процент')),
                ('commission_percent', models.PositiveSmallIntegerField(default=8, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Процент сервиса')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Баланс')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', apps.user.managers.UserManager()),
            ],
        ),
    ]
