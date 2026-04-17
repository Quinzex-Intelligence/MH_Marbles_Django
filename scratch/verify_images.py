import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.products.models import Product
from apps.products.serializers import ProductSerializer

p = Product.objects.first()
if p:
    p.image_keys = ['test/image.jpg']
    p.save()
    s = ProductSerializer(p)
    print(f"Product: {p.name}")
    print(f"Serialized image_url (singular): {s.data.get('image_url')}")
    print(f"Serialized image_urls (plural): {s.data.get('image_urls')}")
else:
    print("No products found.")
