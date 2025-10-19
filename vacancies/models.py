from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Vacancy(models.Model):
    """Модель вакансии"""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Черновик')
        PENDING = 'pending', _('На модерации')
        PUBLISHED = 'published', _('Опубликована')
        CLOSED = 'closed', _('Закрыта')
        REJECTED = 'rejected', _('Отклонена')
    
    class ExperienceLevel(models.TextChoices):
        NO_EXPERIENCE = 'no_experience', _('Без опыта')
        JUNIOR = 'junior', _('Junior (1-3 года)')
        MIDDLE = 'middle', _('Middle (3-5 лет)')
        SENIOR = 'senior', _('Senior (5+ лет)')
        LEAD = 'lead', _('Lead/Team Lead')
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Должность')
    )
    
    description = models.TextField(
        verbose_name=_('Описание')
    )
    
    requirements = models.TextField(
        verbose_name=_('Требования')
    )
    
    responsibilities = models.TextField(
        blank=True,
        verbose_name=_('Обязанности')
    )
    
    salary_min = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Зарплата от')
    )
    
    salary_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Зарплата до')
    )
    
    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.JUNIOR,
        verbose_name=_('Уровень опыта')
    )
    
    company = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name=_('Компания')
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_('Статус')
    )
    
    contact_email = models.EmailField(
        verbose_name=_('Контактный email')
    )
    
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Контактный телефон')
    )
    
    is_remote = models.BooleanField(
        default=False,
        verbose_name=_('Удаленная работа')
    )
    
    auto_close_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Автозакрытие')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )
    
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Дата публикации')
    )
    
    class Meta:
        verbose_name = _('Вакансия')
        verbose_name_plural = _('Вакансии')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.company.company}"
    
    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED
    
    @property
    def is_pending(self):
        return self.status == self.Status.PENDING


class Application(models.Model):
    """Модель отклика на вакансию"""
    
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_('Вакансия')
    )
    
    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications',
        null=True,
        blank=True,
        verbose_name=_('Кандидат')
    )
    
    # Поля для анонимных откликов
    candidate_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Имя кандидата')
    )
    
    candidate_email = models.EmailField(
        blank=True,
        verbose_name=_('Email кандидата')
    )
    
    candidate_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Телефон кандидата')
    )
    
    cover_letter = models.TextField(
        blank=True,
        verbose_name=_('Сопроводительное письмо')
    )
    
    resume_file = models.FileField(
        upload_to='resumes/',
        null=True,
        blank=True,
        verbose_name=_('Файл резюме')
    )
    
    add_to_public_bank = models.BooleanField(
        default=False,
        verbose_name=_('Добавить в общий банк резюме')
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', _('Новый')),
            ('viewed', _('Просмотрен')),
            ('interview', _('Собеседование')),
            ('accepted', _('Принят')),
            ('rejected', _('Отклонен')),
        ],
        default='new',
        verbose_name=_('Статус')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата отклика')
    )
    
    class Meta:
        verbose_name = _('Отклик')
        verbose_name_plural = _('Отклики')
        ordering = ['-created_at']
        # unique_together убран, так как анонимные пользователи не имеют candidate
    
    def __str__(self):
        if self.candidate:
            return f"{self.candidate.get_full_name()} -> {self.vacancy.title}"
        else:
            return f"{self.candidate_name} -> {self.vacancy.title}"
