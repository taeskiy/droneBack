from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet
from apps.category.models import Category
from apps.category.serializers import CategoryTreeSerializer


class CategoryViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = CategoryTreeSerializer
    queryset = Category.objects.all().prefetch_related('children')
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'

    def get_queryset(self):
        if self.action == 'list':
            return Category.objects.filter(parent=None).prefetch_related('children')
        return self.queryset
