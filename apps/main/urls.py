from rest_framework import routers
from apps.main.views import MainPageViewSet, FaqViewSet

main_router = routers.DefaultRouter()
main_router.register(r'mainPage', MainPageViewSet, basename='main_page')
main_router.register(r'faq', FaqViewSet, basename='faq')
