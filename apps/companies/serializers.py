from rest_framework import serializers
from .models import Company
from core.s3 import upload_file

MAX_IMAGES = 5


def _collect_logos(validated_data, folder):
    """Pop logo_1..logo_5 from validated_data, upload each, return list of keys."""
    keys = []
    for i in range(1, MAX_IMAGES + 1):
        img = validated_data.pop(f'logo_{i}', None)
        if img:
            keys.append(upload_file(img, folder))
    return keys


class CompanySerializer(serializers.ModelSerializer):
    logo_urls = serializers.SerializerMethodField()

    # Optional individual logo upload slots
    logo_1 = serializers.ImageField(write_only=True, required=False)
    logo_2 = serializers.ImageField(write_only=True, required=False)
    logo_3 = serializers.ImageField(write_only=True, required=False)
    logo_4 = serializers.ImageField(write_only=True, required=False)
    logo_5 = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Company
        fields = "__all__"
        extra_kwargs = {
            'logo_keys': {'write_only': True, 'required': False}
        }

    def get_logo_urls(self, obj):
        return obj.get_logo_urls()

    def create(self, validated_data):
        keys = _collect_logos(validated_data, "companies")
        if keys:
            validated_data['logo_keys'] = keys
        return super().create(validated_data)

    def update(self, instance, validated_data):
        keys = _collect_logos(validated_data, "companies")
        if keys:
            validated_data['logo_keys'] = keys
        return super().update(instance, validated_data)