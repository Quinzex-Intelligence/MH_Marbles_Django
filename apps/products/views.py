from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from core.s3 import upload_file

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .filters import ProductFilter

from core.pagination import ProductCursorPagination
from core.cache import RedisCacheMixin


class CategoryViewSet(RedisCacheMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None # No pagination for categories usually


class ProductViewSet(RedisCacheMixin, ModelViewSet):

    queryset = Product.objects.all().order_by("-created_at")

    serializer_class = ProductSerializer

    pagination_class = ProductCursorPagination

    filter_backends = [DjangoFilterBackend]

    filterset_class = ProductFilter

    filterset_fields = [
        "company",
        "category",
        "size",
        "color",
        "finish",
        "is_featured",
    ]

    @action(detail=False, methods=["GET"], url_path="featured")
    def featured(self, request):
        """
        Returns up to 6 featured products.
        GET /api/products/featured/
        """
        qs = Product.objects.filter(is_featured=True).order_by("-created_at")[:6]
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], url_path='upload')
    def upload_image(self, request):
        """
        Upload image to S3 and return object key.
        """
        file = request.FILES.get("image")

        if not file:
            return Response({"error": "Image file required"}, status=400)

        key = upload_file(file, "products")

        return Response({
            "key": key
        })