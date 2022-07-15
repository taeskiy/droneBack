from django.db import IntegrityError
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.base.exceptions import droneApiException
from apps.cart.cart_services import CartHelper
from apps.order.models import Order, OrderProduct
from apps.product.serializers import ProductListSerializer


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = OrderProduct
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True)
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    @staticmethod
    def get_products_count(obj):
        return obj.products.count()


class CartProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('quantity', 'product')

    def create(self, validated_data):
        validated_data['order'] = self.initial_data['cart']
        try:
            return OrderProduct.objects.create(**validated_data)
        except IntegrityError as e:
            raise droneApiException('Товар уже добавлен в корзину')


class CartProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('quantity',)


class UserCartProductsField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context['request']
        cart = CartHelper(request).get_cart()
        return cart.products.all()


class CartProductDeleteSerializer(serializers.ModelSerializer):
    products = UserCartProductsField(queryset=OrderProduct.objects.all(),
                                     many=True)

    class Meta:
        model = OrderProduct
        fields = ('products',)

    @atomic
    def destroy(self):
        for item in self.validated_data['products']:
            item.delete()


class CartSmallSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('total', 'products_count')

    @staticmethod
    def get_products_count(obj):
        return obj.products.count()


class CartProductSmallSerializer(serializers.ModelSerializer):
    cart = CartSmallSerializer(source='order')

    class Meta:
        model = OrderProduct
        fields = ('id', 'product', 'quantity', 'cart')
