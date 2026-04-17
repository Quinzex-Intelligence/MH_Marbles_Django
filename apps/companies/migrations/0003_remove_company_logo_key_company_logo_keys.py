from django.db import migrations, models

def migrate_company_logos(apps, schema_editor):
    Company = apps.get_model('companies', 'Company')
    for c in Company.objects.all():
        if hasattr(c, 'logo_key') and c.logo_key:
            c.logo_keys = [c.logo_key]
            c.save()

class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0002_remove_company_logo_company_logo_key"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="logo_keys",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.RunPython(migrate_company_logos, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="company",
            name="logo_key",
        ),
    ]
