from rest_framework import viewsets
from .models import SanitaryProduct
from .serializers import SanitarySerializer, SanitaryCategorySerializer
from apps.products.models import Category


class SanitaryCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("-created_at")
    serializer_class = SanitaryCategorySerializer
    pagination_class = None


class SanitaryProductViewSet(viewsets.ModelViewSet):
    queryset = SanitaryProduct.objects.all().order_by("-created_at")
    serializer_class = SanitarySerializer
    filterset_fields = ["category", "company"]