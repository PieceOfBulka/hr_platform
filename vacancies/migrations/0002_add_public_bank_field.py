# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='add_to_public_bank',
            field=models.BooleanField(default=False, verbose_name='Добавить в общий банк резюме'),
        ),
    ]
