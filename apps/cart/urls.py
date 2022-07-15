from rest_framework import routers
from apps.cart.views import CartViewSet, CartProductViewSet


cart_router = routers.DefaultRouter()
cart_router.register(r'cart', CartViewSet, basename='user_cart')
cart_router.register(r'cartProduct', CartProductViewSet, basename='user_cart_product')
