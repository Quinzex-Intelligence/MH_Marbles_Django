from rest_framework import serializers
from .models import CarouselSlide
from core.s3 import upload_file

MAX_IMAGES = 5


def _collect_images(validated_data, folder, prefix='image'):
    keys = []
    for i in range(1, MAX_IMAGES + 1):
        img = validated_data.pop(f'{prefix}_{i}', None)
        if img:
            keys.append(upload_file(img, folder))
    return keys


class CarouselSlideSerializer(serializers.ModelSerializer):
    image_urls = serializers.SerializerMethodField()
    mobile_image_urls = serializers.SerializerMethodField()

    # Optional individual image upload slots (Desktop)
    image_1 = serializers.ImageField(write_only=True, required=False)
    image_2 = serializers.ImageField(write_only=True, required=False)
    image_3 = serializers.ImageField(write_only=True, required=False)
    image_4 = serializers.ImageField(write_only=True, required=False)
    image_5 = serializers.ImageField(write_only=True, required=False)

    # Optional individual image upload slots (Mobile)
    mobile_image_1 = serializers.ImageField(write_only=True, required=False)
    mobile_image_2 = serializers.ImageField(write_only=True, required=False)
    mobile_image_3 = serializers.ImageField(write_only=True, required=False)
    mobile_image_4 = serializers.ImageField(write_only=True, required=False)
    mobile_image_5 = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = CarouselSlide
        fields = '__all__'
        extra_kwargs = {
            'image_keys': {'write_only': True, 'required': False},
            'mobile_image_keys': {'write_only': True, 'required': False}
        }

    def get_image_urls(self, obj):
        return obj.get_image_urls()

    def get_mobile_image_urls(self, obj):
        return obj.get_mobile_image_urls()

    def validate(self, attrs):
        from django.core.files.images import get_image_dimensions
        
        # Prevent uploading horizontal images for mobile views
        for i in range(1, MAX_IMAGES + 1):
            mobile_img = attrs.get(f'mobile_image_{i}')
            if mobile_img:
                w, h = get_image_dimensions(mobile_img)
                if w and h and w > h:
                    raise serializers.ValidationError({
                        f'mobile_image_{i}': "Horizontal images are not allowed for mobile views. Please upload a vertical image."
                    })
        return attrs

    def create(self, validated_data):
        keys = _collect_images(validated_data, "hero_carousel", prefix="image")
        if keys:
            validated_data['image_keys'] = keys
            
        mobile_keys = _collect_images(validated_data, "hero_carousel", prefix="mobile_image")
        if mobile_keys:
            validated_data['mobile_image_keys'] = mobile_keys
            
        return super().create(validated_data)

    def update(self, instance, validated_data):
        keys = _collect_images(validated_data, "hero_carousel", prefix="image")
        if keys:
            validated_data['image_keys'] = keys
            
        mobile_keys = _collect_images(validated_data, "hero_carousel", prefix="mobile_image")
        if mobile_keys:
            validated_data['mobile_image_keys'] = mobile_keys
            
        return super().update(instance, validated_data)
