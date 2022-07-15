from rest_framework import routers

from apps.category.views import CategoryViewSet

category_router = routers.DefaultRouter()
category_router.register(r'categories', CategoryViewSet, basename='categories')

