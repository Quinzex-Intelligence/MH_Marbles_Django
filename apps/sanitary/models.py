from django.db import models

class SanitaryProduct(models.Model):

    name = models.CharField(max_length=200)

    category = models.ForeignKey(
        "products.Category",
        on_delete=models.CASCADE,
        related_name="sanitary_products",
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)

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