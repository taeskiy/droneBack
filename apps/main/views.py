from rest_framework import mixins, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.main.models import Banner, MainCollections, Faq
from apps.main.serializers import MainPageSerializer, FaqSerializer


class MainPageViewSet(mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = MainPageSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    swagger_tags = ["general"]

    def list(self, request, *args, **kwargs):
        data = {
            'banners': Banner.objects.all(),
            'collections': MainCollections.objects.all(),
        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class FaqViewSet(mixins.ListModelMixin,
                 GenericViewSet):
    serializer_class = FaqSerializer
    queryset = Faq.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    swagger_tags = ["faq"]
