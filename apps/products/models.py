from django.db import models
from django.conf import settings

class Category(models.Model):

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True)

    # Stores up to 5 S3 object keys as a JSON list
    image_keys = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def image_url(self):
        urls = self.get_image_urls()
        return urls[0] if urls else None

    def get_image_urls(self):
        if not self.image_keys:
            return []
        from core.s3 import generate_presigned_url
        return [generate_presigned_url(k) for k in self.image_keys if k]

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=200)

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    size = models.CharField(max_length=50)

    color = models.CharField(max_length=50)

    finish = models.CharField(max_length=50)

    sku = models.CharField(max_length=100, unique=True)

    # Stores up to 5 S3 object keys as a JSON list
    image_keys = models.JSONField(default=list, blank=True)

    is_featured = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def image_url(self):
        urls = self.get_image_urls()
        return urls[0] if urls else None

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.is_featured:
            # Check if we already have 6 featured products
            qs = Product.objects.filter(is_featured=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            
            if qs.count() >= 6:
                raise ValidationError("Only 6 products can be featured at a time.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_image_urls(self):
        if not self.image_keys:
            return []
        from core.s3 import generate_presigned_url
        return [generate_presigned_url(k) for k in self.image_keys if k]

    def __str__(self):
        return self.name