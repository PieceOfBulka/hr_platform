# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internship',
            name='type',
            field=models.CharField(choices=[('internship', 'Стажировка'), ('practice', 'Практика')], default='internship', max_length=20, verbose_name='Тип'),
        ),
        migrations.RenameField(
            model_name='internship',
            old_name='university',
            new_name='organization',
        ),
        migrations.AlterField(
            model_name='internship',
            name='organization',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='internships', to='accounts.user', verbose_name='Организация'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='requirements',
            field=models.TextField(verbose_name='Требования'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='tasks',
            field=models.TextField(blank=True, verbose_name='Задачи'),
        ),
    ]
