from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Internship(models.Model):
    """Модель стажировки/практики"""
    
    class Type(models.TextChoices):
        INTERNSHIP = 'internship', _('Стажировка')
        PRACTICE = 'practice', _('Практика')
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Черновик')
        PENDING = 'pending', _('На модерации')
        PUBLISHED = 'published', _('Опубликована')
        CLOSED = 'closed', _('Закрыта')
        REJECTED = 'rejected', _('Отклонена')
    
    class Duration(models.TextChoices):
        ONE_MONTH = '1', _('1 месяц')
        TWO_MONTHS = '2', _('2 месяца')
        THREE_MONTHS = '3', _('3 месяца')
        SIX_MONTHS = '6', _('6 месяцев')
        ONE_YEAR = '12', _('1 год')
    
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.INTERNSHIP,
        verbose_name=_('Тип')
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Название')
    )
    
    description = models.TextField(
        verbose_name=_('Описание')
    )
    
    requirements = models.TextField(
        verbose_name=_('Требования')
    )
    
    tasks = models.TextField(
        blank=True,
        verbose_name=_('Задачи')
    )
    
    specialization = models.CharField(
        max_length=200,
        verbose_name=_('Специальность')
    )
    
    students_count = models.PositiveIntegerField(
        verbose_name=_('Количество студентов')
    )
    
    duration = models.CharField(
        max_length=10,
        choices=Duration.choices,
        default=Duration.THREE_MONTHS,
        verbose_name=_('Продолжительность')
    )
    
    start_date = models.DateField(
        verbose_name=_('Дата начала')
    )
    
    end_date = models.DateField(
        verbose_name=_('Дата окончания')
    )
    
    organization = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='internships',
        verbose_name=_('Организация')
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
        verbose_name=_('Удаленная стажировка')
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
        verbose_name = _('Стажировка')
        verbose_name_plural = _('Стажировки')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.organization.company}"
    
    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED
    
    @property
    def is_pending(self):
        return self.status == self.Status.PENDING


class InternshipApplication(models.Model):
    """Модель заявки на стажировку"""
    
    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_('Стажировка')
    )
    
    company = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='internship_applications',
        verbose_name=_('Компания')
    )
    
    message = models.TextField(
        blank=True,
        verbose_name=_('Сообщение')
    )
    
    students_count = models.PositiveIntegerField(
        verbose_name=_('Количество студентов')
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', _('Новая')),
            ('viewed', _('Просмотрена')),
            ('accepted', _('Принята')),
            ('rejected', _('Отклонена')),
        ],
        default='new',
        verbose_name=_('Статус')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата заявки')
    )
    
    class Meta:
        verbose_name = _('Заявка на стажировку')
        verbose_name_plural = _('Заявки на стажировки')
        ordering = ['-created_at']
        unique_together = ['internship', 'company']
    
    def __str__(self):
        return f"{self.company.company} -> {self.internship.title}"
