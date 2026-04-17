from django.db import migrations, models

def migrate_carousel_images(apps, schema_editor):
    CarouselSlide = apps.get_model('hero_carousel', 'CarouselSlide')
    for cs in CarouselSlide.objects.all():
        if hasattr(cs, 'image_key') and cs.image_key:
            cs.image_keys = [cs.image_key]
            cs.save()

class Migration(migrations.Migration):

    dependencies = [
        ("hero_carousel", "0002_remove_carouselslide_image_carouselslide_image_key"),
    ]

    operations = [
        migrations.AddField(
            model_name="carouselslide",
            name="image_keys",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.RunPython(migrate_carousel_images, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="carouselslide",
            name="image_key",
        ),
    ]
