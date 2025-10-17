from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Resume(models.Model):
    """Модель резюме"""
    
    class ExperienceLevel(models.TextChoices):
        NO_EXPERIENCE = 'no_experience', _('Без опыта')
        JUNIOR = 'junior', _('Junior (1-3 года)')
        MIDDLE = 'middle', _('Middle (3-5 лет)')
        SENIOR = 'senior', _('Senior (5+ лет)')
        LEAD = 'lead', _('Lead/Team Lead')
    
    class EducationLevel(models.TextChoices):
        SECONDARY = 'secondary', _('Среднее')
        SPECIALIZED = 'specialized', _('Среднее специальное')
        BACHELOR = 'bachelor', _('Бакалавр')
        MASTER = 'master', _('Магистр')
        PHD = 'phd', _('Кандидат наук')
        DOCTOR = 'doctor', _('Доктор наук')
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='resume',
        verbose_name=_('Пользователь')
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Желаемая должность')
    )
    
    summary = models.TextField(
        blank=True,
        verbose_name=_('О себе')
    )
    
    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.JUNIOR,
        verbose_name=_('Уровень опыта')
    )
    
    education_level = models.CharField(
        max_length=20,
        choices=EducationLevel.choices,
        default=EducationLevel.BACHELOR,
        verbose_name=_('Уровень образования')
    )
    
    university = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Университет')
    )
    
    faculty = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Факультет')
    )
    
    graduation_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Год окончания')
    )
    
    skills = models.TextField(
        blank=True,
        verbose_name=_('Навыки')
    )
    
    languages = models.TextField(
        blank=True,
        verbose_name=_('Языки')
    )
    
    salary_expectation = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Желаемая зарплата')
    )
    
    is_remote = models.BooleanField(
        default=False,
        verbose_name=_('Готов к удаленной работе')
    )
    
    is_relocation = models.BooleanField(
        default=False,
        verbose_name=_('Готов к переезду')
    )
    
    resume_file = models.FileField(
        upload_to='resumes/',
        null=True,
        blank=True,
        verbose_name=_('Файл резюме')
    )
    
    is_public = models.BooleanField(
        default=True,
        verbose_name=_('Публичное резюме')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )
    
    class Meta:
        verbose_name = _('Резюме')
        verbose_name_plural = _('Резюме')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.title}"


class WorkExperience(models.Model):
    """Модель опыта работы"""
    
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='work_experiences',
        verbose_name=_('Резюме')
    )
    
    company = models.CharField(
        max_length=200,
        verbose_name=_('Компания')
    )
    
    position = models.CharField(
        max_length=200,
        verbose_name=_('Должность')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Описание')
    )
    
    start_date = models.DateField(
        verbose_name=_('Дата начала')
    )
    
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Дата окончания')
    )
    
    is_current = models.BooleanField(
        default=False,
        verbose_name=_('Текущее место работы')
    )
    
    class Meta:
        verbose_name = _('Опыт работы')
        verbose_name_plural = _('Опыт работы')
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.position} в {self.company}"


class Education(models.Model):
    """Модель образования"""
    
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='educations',
        verbose_name=_('Резюме')
    )
    
    institution = models.CharField(
        max_length=200,
        verbose_name=_('Учебное заведение')
    )
    
    degree = models.CharField(
        max_length=200,
        verbose_name=_('Степень/Специальность')
    )
    
    start_date = models.DateField(
        verbose_name=_('Дата начала')
    )
    
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Дата окончания')
    )
    
    is_current = models.BooleanField(
        default=False,
        verbose_name=_('Текущее обучение')
    )
    
    class Meta:
        verbose_name = _('Образование')
        verbose_name_plural = _('Образование')
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.degree} в {self.institution}"
