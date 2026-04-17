from django.db import migrations, models

def migrate_sanitary_images(apps, schema_editor):
    SanitaryProduct = apps.get_model('sanitary', 'SanitaryProduct')
    for sp in SanitaryProduct.objects.all():
        if hasattr(sp, 'image_key') and sp.image_key:
            sp.image_keys = [sp.image_key]
            sp.save()

class Migration(migrations.Migration):

    dependencies = [
        ("sanitary", "0003_alter_sanitaryproduct_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sanitaryproduct",
            name="image_keys",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.RunPython(migrate_sanitary_images, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="sanitaryproduct",
            name="image_key",
        ),
    ]
