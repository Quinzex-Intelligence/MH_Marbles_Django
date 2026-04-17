from django.db import migrations, models

def migrate_product_images(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    for p in Product.objects.all():
        if hasattr(p, 'image_key') and p.image_key:
            p.image_keys = [p.image_key]
            p.save()

def migrate_category_images(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    for c in Category.objects.all():
        if hasattr(c, 'image_key') and c.image_key:
            c.image_keys = [c.image_key]
            c.save()

class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_category_created_at"),
    ]

    operations = [
        # 1. Add new fields
        migrations.AddField(
            model_name="category",
            name="image_keys",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="product",
            name="image_keys",
            field=models.JSONField(blank=True, default=list),
        ),
        # 2. Migrate data
        migrations.RunPython(migrate_category_images, migrations.RunPython.noop),
        migrations.RunPython(migrate_product_images, migrations.RunPython.noop),
        # 3. Remove old fields
        migrations.RemoveField(
            model_name="category",
            name="image_key",
        ),
        migrations.RemoveField(
            model_name="product",
            name="image_key",
        ),
        # 4. Miscellaneous changes
        migrations.AlterField(
            model_name="category",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
