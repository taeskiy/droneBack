from django.db import models


class OrderUser(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name} - {self.phone}'


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    STATUS_CART = 'CART'
    STATUS_NEW = 'NEW'
    STATUS_APPROVED = 'APPROVED'
    STATUS_DONE = 'DONE'
    STATUS_CHOICES = (
        (STATUS_CART, 'В корзине'),
        (STATUS_NEW, 'Новый'),
        (STATUS_APPROVED, 'Подтвержденный'),
        (STATUS_DONE, 'Завершен'),
    )
    imei = models.CharField(max_length=512, null=True, blank=True)
    date = models.DateTimeField('Дата создания', auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_NEW, max_length=24)
    total = models.DecimalField(default=0.0, max_digits=16, decimal_places=2)
    user = models.ForeignKey('OrderUser', models.PROTECT, related_name='orders', null=True, blank=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.imei}'


class OrderProduct(models.Model):
    order = models.ForeignKey('Order', models.CASCADE, related_name='products')
    product = models.ForeignKey('product.Product', models.PROTECT, related_name='order_products')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(default=0.0, max_digits=16, decimal_places=2)
    amount = models.DecimalField(default=0.0, max_digits=16, decimal_places=2)

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = ('order', 'product')
