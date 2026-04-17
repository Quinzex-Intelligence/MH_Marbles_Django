from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("name", "company", "category", "size", "finish", "is_featured")

    search_fields = ("name", "sku")

    list_filter = ("company", "category", "finish", "is_featured")
    
    list_editable = ("is_featured",)


admin.site.register(Category)