from rest_framework import routers
from .views import ProductViewSet, RestaurantViewSet

product_router = routers.DefaultRouter()
product_router.register(r'products', ProductViewSet, basename='product')
product_router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
