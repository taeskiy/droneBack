from functools import cache

from django.db.transaction import atomic
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.base.exceptions import droneApiException
from apps.cart.cart_calculations import CartCalculation
from apps.cart.cart_services import CartHelper
from apps.cart.permissions import CartPermission
from apps.cart.serializers import CartSerializer, CartProductCreateSerializer, \
    CartProductSmallSerializer, CartProductUpdateSerializer, CartProductSerializer
from apps.order.models import OrderProduct, Order


imei_parameter = openapi.Parameter(
    'imei', openapi.IN_HEADER,
    description="imei of device",
    required=True,
    type=openapi.TYPE_STRING, default='some_random_uuid'
)


class CartViewSet(mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = CartSerializer
    queryset = Order.objects.all().prefetch_related('products')
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    swagger_tags = ['cart']

    def get_serializer_class(self):
        if self.action == 'add_product':
            return CartProductCreateSerializer
        return self.serializer_class

    @cache
    def get_object(self):
        return CartHelper(self.request).get_cart()

    @swagger_auto_schema(manual_parameters=[imei_parameter])
    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(manual_parameters=[imei_parameter])
    @action(['DELETE'], False, 'emptyCart')
    def empty_cart(self, request, *args, **kwargs):
        helper = CartHelper(self.request)
        helper.empty_cart()
        CartCalculation(helper.get_cart()).recalculate()
        return Response({"message": "ok"})


class CartProductViewSet(mixins.DestroyModelMixin,
                         GenericViewSet):
    serializer_class = CartProductSerializer
    permission_classes = [CartPermission]
    swagger_tags = ['cart']

    def get_queryset(self):
        imei = self.request.headers.get('imei', None)
        return OrderProduct.objects.filter(order__imei=imei)

    def get_serializer_class(self):
        serializers_map = {
            'create': CartProductCreateSerializer,
            'update': CartProductUpdateSerializer,
        }
        return serializers_map.get(self.action, self.serializer_class)

    @atomic
    @swagger_auto_schema(manual_parameters=[imei_parameter],
                         responses={200: CartProductSmallSerializer})
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['cart'] = CartHelper(request).get_cart()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        CartCalculation(instance.order).recalculate()
        return Response(
            CartProductSmallSerializer(instance).data
        )

    @atomic
    @swagger_auto_schema(manual_parameters=[imei_parameter],
                         responses={200: CartProductSmallSerializer})
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        CartCalculation(instance.order).recalculate()
        return Response(
            CartProductSmallSerializer(instance).data
        )

    @atomic
    @swagger_auto_schema(manual_parameters=[imei_parameter],
                         responses={200: CartProductSmallSerializer})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        CartCalculation(instance.order).recalculate()
        return Response(
            CartProductSmallSerializer(instance).data
        )
