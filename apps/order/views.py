from django.db.models import Q, Count
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins
from apps.base.exceptions import droneApiException
from apps.order.models import Order, OrderProduct
from apps.order.serializers import OrderListSerializer, OrderSerializer, OrderRetrieveSerializer, OrderUserCreateSerializer

imei_parameter = openapi.Parameter(
    'imei', openapi.IN_HEADER,
    description="imei of device",
    required=True,
    type=openapi.TYPE_STRING, default='some_random_uuid'
)


@method_decorator(name='list', decorator=swagger_auto_schema(
    manual_parameters=[imei_parameter]
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    manual_parameters=[imei_parameter]
))
class OrderViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        serializer_map = {
            'list': OrderListSerializer,
            'retrieve': OrderRetrieveSerializer,
            'init_order': OrderUserCreateSerializer
        }
        return serializer_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        imei = self.request.headers.get('imei', None)
        if not imei:
            raise droneApiException('imei is required')

        queryset = Order.objects.filter(
            ~Q(status__in=[Order.STATUS_CART]),
            imei=imei,
        ).annotate(
            product_count=Count('products'),
        )
        if self.action == 'retrieve':
            queryset.prefetch_related('products')
        return queryset

    def get_cart_order(self):
        imei = self.request.headers.get('imei', None)
        if not imei:
            raise droneApiException('imei is required')
        return Order.objects.filter(status=Order.STATUS_CART, imei=imei).first()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['order'] = self.get_cart_order()
        return context

    @swagger_auto_schema(request_body=OrderUserCreateSerializer,
                         manual_parameters=[imei_parameter])
    @action(['PUT'], False, 'initOrder')
    def init_order(self, request):
        order = self.get_cart_order()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        order.refresh_from_db()
        return Response(
            OrderRetrieveSerializer(order,
                                    context=self.get_serializer_context()).data
        )
