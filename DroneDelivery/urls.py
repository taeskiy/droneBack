from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from DroneDelivery import settings
from apps.cart.urls import cart_router
from apps.category.urls import category_router
from apps.main.urls import main_router
from apps.order.urls import order_router
from apps.product.urls import product_router

router = routers.DefaultRouter()
# router.registry.extend(category_router.registry)
router.registry.extend(product_router.registry)
# router.registry.extend(main_router.registry)
router.registry.extend(cart_router.registry)
router.registry.extend(order_router.registry)


urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/admin/', admin.site.urls),
]

if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="DroneDelivery API",
            default_version='v1',
            description="DroneDelivery Python API",
            terms_of_service="",
            contact=openapi.Contact(email="eldosatalov@gmail.com"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns = urlpatterns + [
        path(r'api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path(r'api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
