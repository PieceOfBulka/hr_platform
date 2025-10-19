# Generated manually

from django.db import migrations

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('internships', '0002_update_models_structure'),
    ]

    operations = [
        migrations.RunPython(noop),
    ]