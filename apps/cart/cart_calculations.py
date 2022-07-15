from decimal import Decimal
from functools import cached_property
from apps.base.exceptions import droneApiException
from apps.order.models import Order


class CartCalculation:
    def __init__(self, cart: Order):
        if cart.status not in [Order.STATUS_CART]:
            raise droneApiException('Нельзя пересчитывать заказ после завершения')
        self._cart = cart

    def recalculate(self):
        self._cart.total = self._get_product_total()
        self._save()

    def _save(self):
        self._cart.save()

    def _get_product_total(self) -> Decimal:
        products = self._cart.products.all().select_related('product')
        total_sum = Decimal(0)
        for item in products:
            item.price = item.product.price
            item.amount = Decimal(item.price * item.quantity)
            item.save()
            total_sum += item.amount

        return Decimal(total_sum)
