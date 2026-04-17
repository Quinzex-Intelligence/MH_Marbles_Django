from rest_framework import serializers
from .models import ProductCollection
from core.s3 import upload_file

MAX_IMAGES = 5


def _collect_images(validated_data, folder):
    keys = []
    for i in range(1, MAX_IMAGES + 1):
        img = validated_data.pop(f'image_{i}', None)
        if img:
            keys.append(upload_file(img, folder))
    return keys


class ProductCollectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    image_urls = serializers.SerializerMethodField()

    # Optional individual image upload slots
    image_1 = serializers.ImageField(write_only=True, required=False)
    image_2 = serializers.ImageField(write_only=True, required=False)
    image_3 = serializers.ImageField(write_only=True, required=False)
    image_4 = serializers.ImageField(write_only=True, required=False)
    image_5 = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = ProductCollection
        fields = "__all__"
        extra_kwargs = {
            'image_keys': {'required': False}
        }

    def get_image_url(self, obj):
        return obj.image_url

    def get_image_urls(self, obj):
        return obj.get_image_urls()

    def create(self, validated_data):
        keys = _collect_images(validated_data, "collections")
        if keys:
            validated_data['image_keys'] = keys
        return super().create(validated_data)

    def update(self, instance, validated_data):
        keys = _collect_images(validated_data, "collections")
        if keys:
            validated_data['image_keys'] = keys
        return super().update(instance, validated_data)