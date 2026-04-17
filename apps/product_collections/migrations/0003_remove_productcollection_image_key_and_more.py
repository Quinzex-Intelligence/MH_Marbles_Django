from django.db import migrations, models

def migrate_collection_images(apps, schema_editor):
    ProductCollection = apps.get_model('product_collections', 'ProductCollection')
    for pc in ProductCollection.objects.all():
        if hasattr(pc, 'image_key') and pc.image_key:
            pc.image_keys = [pc.image_key]
            pc.save()

class Migration(migrations.Migration):

    dependencies = [
        ("product_collections", "0002_remove_productcollection_cover_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productcollection",
            name="image_keys",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.RunPython(migrate_collection_images, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="productcollection",
            name="image_key",
        ),
    ]
