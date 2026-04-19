from rest_framework import viewsets
from .models import CarouselSlide
from .serializers import CarouselSlideSerializer
from core.cache import RedisCacheMixin

class CarouselSlideViewSet(RedisCacheMixin, viewsets.ModelViewSet):
    queryset = CarouselSlide.objects.all()
    serializer_class = CarouselSlideSerializer
