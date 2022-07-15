from rest_framework import serializers

from apps.category.models import Category


class ShortCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'parent', 'level', 'icon')


class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    @staticmethod
    def get_children(obj):
        if obj.children.exists():
            return CategoryTreeSerializer(obj.children.all(), many=True).data
        return None

