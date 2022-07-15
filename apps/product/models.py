import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class Restaurant(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=256)
    lng = models.CharField(null=True, blank=True, max_length=128)
    lnt = models.CharField(null=True, blank=True, max_length=128)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey('Restaurant', models.PROTECT, null=True)
    title = models.CharField('Название товара', max_length=255)
    description = models.CharField('Короткое описание', max_length=512)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    price = models.DecimalField('Цена', default=1.0, max_digits=16, decimal_places=2, validators=[MinValueValidator(1)])
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-id']

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    class Meta:
        verbose_name = 'Фото для товара'
        verbose_name_plural = 'Фото для товаров'
        ordering = ['id']

    image = models.ImageField('Фотография', upload_to='products', blank=True, null=True)
    product = models.ForeignKey('Product', verbose_name='Товар', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.title + str(self.id)
