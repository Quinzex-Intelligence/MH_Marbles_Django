from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=150)
    # Stores up to 5 S3 object keys as a JSON list
    logo_keys = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_logo_urls(self):
        if not self.logo_keys:
            return []
        from core.s3 import generate_presigned_url
        return [generate_presigned_url(k) for k in self.logo_keys if k]

    def __str__(self):
        return self.name