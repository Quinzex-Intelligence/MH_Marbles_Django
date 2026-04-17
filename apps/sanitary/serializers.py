from rest_framework import serializers
from .models import SanitaryProduct
from apps.products.models import Category
from core.s3 import upload_file

MAX_IMAGES = 5


def _collect_images(validated_data, folder):
    keys = []
    for i in range(1, MAX_IMAGES + 1):
        img = validated_data.pop(f'image_{i}', None)
        if img:
            keys.append(upload_file(img, folder))
    return keys


class SanitaryCategorySerializer(serializers.ModelSerializer):
    image_urls = serializers.SerializerMethodField()

    # Optional individual image upload slots
    image_1 = serializers.ImageField(write_only=True, required=False)
    image_2 = serializers.ImageField(write_only=True, required=False)
    image_3 = serializers.ImageField(write_only=True, required=False)
    image_4 = serializers.ImageField(write_only=True, required=False)
    image_5 = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            'image_keys': {'write_only': True, 'required': False}
        }


    def get_image_urls(self, obj):
        return obj.get_image_urls()

    def create(self, validated_data):
        keys = _collect_images(validated_data, "sanitary/categories")
        if keys:
            validated_data['image_keys'] = keys
        return super().create(validated_data)

    def update(self, instance, validated_data):
        keys = _collect_images(validated_data, "sanitary/categories")
        if keys:
            validated_data['image_keys'] = keys
        return super().update(instance, validated_data)


class SanitarySerializer(serializers.ModelSerializer):
    image_urls = serializers.SerializerMethodField()

    # Optional individual image upload slots
    image_1 = serializers.ImageField(write_only=True, required=False)
    image_2 = serializers.ImageField(write_only=True, required=False)
    image_3 = serializers.ImageField(write_only=True, required=False)
    image_4 = serializers.ImageField(write_only=True, required=False)
    image_5 = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = SanitaryProduct
        fields = "__all__"
        extra_kwargs = {
            'image_keys': {'write_only': True, 'required': False}
        }


    def get_image_urls(self, obj):
        return obj.get_image_urls()

    def create(self, validated_data):
        keys = _collect_images(validated_data, "sanitary/products")
        if keys:
            validated_data['image_keys'] = keys
        return super().create(validated_data)

    def update(self, instance, validated_data):
        keys = _collect_images(validated_data, "sanitary/products")
        if keys:
            validated_data['image_keys'] = keys
        return super().update(instance, validated_data)