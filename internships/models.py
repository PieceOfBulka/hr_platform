from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Internship(models.Model):
    """Модель стажировки (размещается HR)"""
    
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
    
    company = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='internships',
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
        return f"{self.title} - {self.company.company}"
    
    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED
    
    @property
    def is_pending(self):
        return self.status == self.Status.PENDING


class PracticeRequest(models.Model):
    """Модель заявки на практику (размещается представителем вуза)"""
    
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
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Название практики')
    )
    
    description = models.TextField(
        verbose_name=_('Описание')
    )
    
    requirements = models.TextField(
        verbose_name=_('Требования к студентам')
    )
    
    tasks = models.TextField(
        blank=True,
        verbose_name=_('Задачи практики')
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
    
    university = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='practice_requests',
        verbose_name=_('Университет')
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
        verbose_name=_('Удаленная практика')
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
        verbose_name = _('Заявка на практику')
        verbose_name_plural = _('Заявки на практику')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.university.company}"
    
    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED
    
    @property
    def is_pending(self):
        return self.status == self.Status.PENDING


class InternshipApplication(models.Model):
    """Модель отклика соискателя на стажировку"""
    
    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_('Стажировка')
    )
    
    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='internship_applications',
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
        verbose_name = _('Отклик на стажировку')
        verbose_name_plural = _('Отклики на стажировки')
        ordering = ['-created_at']
    
    def __str__(self):
        if self.candidate:
            return f"{self.candidate.get_full_name()} -> {self.internship.title}"
        else:
            return f"{self.candidate_name} -> {self.internship.title}"


class PracticeApplication(models.Model):
    """Модель отклика HR на заявку вуза на практику"""
    
    practice_request = models.ForeignKey(
        PracticeRequest,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_('Заявка на практику')
    )
    
    hr_company = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='practice_applications',
        verbose_name=_('HR компании')
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
        verbose_name = _('Отклик на заявку практики')
        verbose_name_plural = _('Отклики на заявки практики')
        ordering = ['-created_at']
        unique_together = ['practice_request', 'hr_company']
    
    def __str__(self):
        return f"{self.hr_company.company} -> {self.practice_request.title}"
