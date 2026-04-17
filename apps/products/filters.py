import django_filters
from django.db.models import Q

from .models import Product


class ProductFilter(django_filters.FilterSet):

    company = django_filters.NumberFilter(field_name="company")

    category = django_filters.CharFilter(
        field_name="category",
        lookup_expr="icontains"
    )

    size = django_filters.CharFilter(
        field_name="size",
        lookup_expr="icontains"
    )

    color = django_filters.CharFilter(
        field_name="color",
        lookup_expr="icontains"
    )

    finish = django_filters.CharFilter(
        field_name="finish",
        lookup_expr="icontains"
    )

    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = Product
        fields = [
            "company",
            "category",
            "size",
            "color",
            "finish",
            "is_featured",
        ]

    def filter_search(self, queryset, name, value):

        return queryset.filter(
            Q(name__icontains=value) |
            Q(sku__icontains=value)
        )