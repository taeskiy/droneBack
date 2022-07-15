from functools import cache
from apps.base.exceptions import droneApiException
from apps.order.models import Order


class CartHelper:
    def __init__(self, request):
        self._request = request
        self._imei = request.headers.get('imei', None)
        if not self._imei:
            raise droneApiException('imei is required')

    @cache
    def get_cart(self, check_if_empty=False):
        cart, created = Order.objects.get_or_create(imei=self._imei,
                                                    status=Order.STATUS_CART)

        if check_if_empty:
            if cart.products.count() == 0:
                raise droneApiException('Корзина пуста')
        return cart

    def empty_cart(self):
        cart = self.get_cart()
        cart.products.all().delete()

