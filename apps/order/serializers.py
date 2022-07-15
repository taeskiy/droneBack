from rest_framework import serializers

from apps.order.models import Order, OrderUser, OrderProduct
from apps.product.serializers import ProductListSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderUser
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        order = self.context['order']
        order.user = user
        order.status = Order.STATUS_NEW
        order.save()
        return user


class OrderListSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField()
    user = OrderUserCreateSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = OrderProduct
        fields = ('id', 'quantity', 'price', 'amount', 'product')


class OrderRetrieveSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    user = OrderUserCreateSerializer()

    class Meta:
        model = Order
        fields = '__all__'

