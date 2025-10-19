# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('internships', '0002_internship_type_organization'),
    ]

    operations = [
        # Удаляем старое поле type из Internship
        migrations.RemoveField(
            model_name='internship',
            name='type',
        ),
        
        # Удаляем старое поле students_count из Internship
        migrations.RemoveField(
            model_name='internship',
            name='students_count',
        ),
        
        # Переименовываем поле organization в company для Internship
        migrations.RenameField(
            model_name='internship',
            old_name='organization',
            new_name='company',
        ),
        
        # Создаем новую модель PracticeRequest
        migrations.CreateModel(
            name='PracticeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название практики')),
                ('description', models.TextField(verbose_name='Описание')),
                ('requirements', models.TextField(verbose_name='Требования к студентам')),
                ('tasks', models.TextField(blank=True, verbose_name='Задачи практики')),
                ('specialization', models.CharField(max_length=200, verbose_name='Специальность')),
                ('students_count', models.PositiveIntegerField(verbose_name='Количество студентов')),
                ('duration', models.CharField(choices=[('1', '1 месяц'), ('2', '2 месяца'), ('3', '3 месяца'), ('6', '6 месяцев'), ('12', '1 год')], default='3', max_length=10, verbose_name='Продолжительность')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
                ('status', models.CharField(choices=[('draft', 'Черновик'), ('pending', 'На модерации'), ('published', 'Опубликована'), ('closed', 'Закрыта'), ('rejected', 'Отклонена')], default='draft', max_length=20, verbose_name='Статус')),
                ('contact_email', models.EmailField(verbose_name='Контактный email')),
                ('contact_phone', models.CharField(blank=True, max_length=20, verbose_name='Контактный телефон')),
                ('is_remote', models.BooleanField(default=False, verbose_name='Удаленная практика')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practice_requests', to='accounts.user', verbose_name='Университет')),
            ],
            options={
                'verbose_name': 'Заявка на практику',
                'verbose_name_plural': 'Заявки на практику',
                'ordering': ['-created_at'],
            },
        ),
        
        # Обновляем модель InternshipApplication
        migrations.RemoveField(
            model_name='internshipapplication',
            name='company',
        ),
        migrations.RemoveField(
            model_name='internshipapplication',
            name='message',
        ),
        migrations.RemoveField(
            model_name='internshipapplication',
            name='students_count',
        ),
        migrations.AddField(
            model_name='internshipapplication',
            name='candidate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='internship_applications', to='accounts.user', verbose_name='Кандидат'),
        ),
        migrations.AddField(
            model_name='internshipapplication',
            name='candidate_email',
            field=models.EmailField(blank=True, verbose_name='Email кандидата'),
        ),
        migrations.AddField(
            model_name='internshipapplication',
            name='candidate_name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Имя кандидата'),
        ),
        migrations.AddField(
            model_name='internshipapplication',
            name='candidate_phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Телефон кандидата'),
        ),
        migrations.AddField(
            model_name='internshipapplication',
            name='cover_letter',
            field=models.TextField(blank=True, verbose_name='Сопроводительное письмо'),
        ),
        migrations.AddField(
            model_name='internshipapplication',
            name='resume_file',
            field=models.FileField(blank=True, null=True, upload_to='resumes/', verbose_name='Файл резюме'),
        ),
        migrations.AlterField(
            model_name='internshipapplication',
            name='status',
            field=models.CharField(choices=[('new', 'Новый'), ('viewed', 'Просмотрен'), ('interview', 'Собеседование'), ('accepted', 'Принят'), ('rejected', 'Отклонен')], default='new', max_length=20, verbose_name='Статус'),
        ),
        migrations.AlterModelOptions(
            name='internshipapplication',
            options={'ordering': ['-created_at'], 'verbose_name': 'Отклик на стажировку', 'verbose_name_plural': 'Отклики на стажировки'},
        ),
        migrations.RemoveConstraint(
            model_name='internshipapplication',
            name='internships_internshipapplication_unique',
        ),
        
        # Создаем новую модель PracticeApplication
        migrations.CreateModel(
            name='PracticeApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, verbose_name='Сообщение')),
                ('students_count', models.PositiveIntegerField(verbose_name='Количество студентов')),
                ('status', models.CharField(choices=[('new', 'Новая'), ('viewed', 'Просмотрена'), ('accepted', 'Принята'), ('rejected', 'Отклонена')], default='new', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата заявки')),
                ('hr_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practice_applications', to='accounts.user', verbose_name='HR компании')),
                ('practice_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='internships.practicerequest', verbose_name='Заявка на практику')),
            ],
            options={
                'verbose_name': 'Отклик на заявку практики',
                'verbose_name_plural': 'Отклики на заявки практики',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='practiceapplication',
            constraint=models.UniqueConstraint(fields=('practice_request', 'hr_company'), name='internships_practiceapplication_unique'),
        ),
    ]
