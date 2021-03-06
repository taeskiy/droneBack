# Generated by Django 3.2.2 on 2021-10-01 09:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Название товара')),
                ('description', models.CharField(max_length=512, verbose_name='Короткое описание')),
                ('image_url', models.URLField(blank=True, null=True, verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, default=1.0, max_digits=16, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Цена')),
                ('search', models.CharField(default='', max_length=512, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('measure', models.CharField(max_length=32)),
                ('is_active', models.BooleanField(blank=True, default=None, null=True, verbose_name='Активный')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=1024, unique=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='category.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products', verbose_name='Фотография')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Фото для товара',
                'verbose_name_plural': 'Фото для товаров',
                'ordering': ['id'],
            },
        ),
    ]
