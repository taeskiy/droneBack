from rest_framework import serializers

from apps.product.models import Product, ProductImage, Restaurant


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
