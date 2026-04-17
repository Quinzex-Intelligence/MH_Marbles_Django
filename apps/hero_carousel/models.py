from django.db import models

class CarouselSlide(models.Model):
    # Stores up to 5 S3 object keys as a JSON list
    image_keys = models.JSONField(default=list, blank=True)
    heading = models.CharField(max_length=200, blank=True)
    subtext = models.CharField(max_length=300, blank=True)
    cta_text = models.CharField(max_length=50, blank=True)
    cta_link = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_image_urls(self):
        if not self.image_keys:
            return []
        from core.s3 import generate_presigned_url
        return [generate_presigned_url(k) for k in self.image_keys if k]

    def __str__(self):
        return self.heading or f"Slide {self.order}"
    
    class Meta:
        ordering = ['order', '-created_at']
