from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.cart.cart_services import CartHelper
from apps.cart.serializers import CartProductSerializer
from apps.order.models import OrderProduct
from apps.order.views import imei_parameter
from apps.product.models import Product, Restaurant
from apps.product.serializers import ProductDetailSerializer, ProductListSerializer, RestaurantSerializer


class ProductViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['price']
    filterset_fields = {
        'restaurant': ['exact']
    }
    search_fields = ['title',  'description', 'search']

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @swagger_auto_schema(manual_parameters=[imei_parameter])
    @action(['GET'], True, 'cartProduct')
    def get_cart_product(self, request, pk):
        cart = CartHelper(request).get_cart()
        cart_product = get_object_or_404(OrderProduct, product=self.get_object(),
                                         order=cart)
        return Response(
            CartProductSerializer(
                cart_product,
                context=self.get_serializer_context()
            ).data
        )


class RestaurantViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
