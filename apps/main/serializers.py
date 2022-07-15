from rest_framework import serializers

from apps.main.models import CollectionProducts, MainCollections, Banner, Faq
from apps.product.serializers import ProductListSerializer


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class CollectionProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionProducts
        exclude = ('collection',)

    def to_representation(self, instance):
        return ProductListSerializer(instance.product, context=self.context).data


class CollectionsSerializer(serializers.ModelSerializer):
    products = CollectionProductsSerializer(many=True)

    class Meta:
        model = MainCollections
        fields = ('id', 'title', 'category', 'products')


class MainPageSerializer(serializers.Serializer):
    banners = BannerSerializer(many=True)
    collections = CollectionsSerializer(many=True)


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        exclude = ('my_order',)
