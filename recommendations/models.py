from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from vacancies.models import Vacancy, Application
from resumes.models import Resume

User = get_user_model()


class RecommendationRule(models.Model):
    """Правило рекомендации"""
    
    name = models.CharField(
        max_length=200,
        verbose_name=_('Название правила')
    )
    
    description = models.TextField(
        verbose_name=_('Описание правила')
    )
    
    skill_keywords = models.TextField(
        blank=True,
        help_text=_('Ключевые слова навыков через запятую'),
        verbose_name=_('Ключевые слова навыков')
    )
    
    experience_level = models.CharField(
        max_length=20,
        choices=Vacancy.ExperienceLevel.choices,
        blank=True,
        verbose_name=_('Уровень опыта')
    )
    
    salary_min = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Минимальная зарплата')
    )
    
    salary_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Максимальная зарплата')
    )
    
    is_remote = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('Удаленная работа')
    )
    
    weight = models.FloatField(
        default=1.0,
        verbose_name=_('Вес правила')
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Активно')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    
    class Meta:
        verbose_name = _('Правило рекомендации')
        verbose_name_plural = _('Правила рекомендаций')
        ordering = ['-weight', '-created_at']
    
    def __str__(self):
        return self.name


class ResumeRecommendation(models.Model):
    """Рекомендация резюме для вакансии"""
    
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='resume_recommendations',
        verbose_name=_('Вакансия')
    )
    
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='vacancy_recommendations',
        verbose_name=_('Резюме')
    )
    
    score = models.FloatField(
        verbose_name=_('Оценка совпадения')
    )
    
    matched_rules = models.TextField(
        default='[]',
        verbose_name=_('Совпавшие правила')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    
    class Meta:
        verbose_name = _('Рекомендация резюме')
        verbose_name_plural = _('Рекомендации резюме')
        ordering = ['-score', '-created_at']
        unique_together = ['vacancy', 'resume']
    
    def __str__(self):
        return f"{self.resume.title} -> {self.vacancy.title} ({self.score:.2f})"


class HRRecommendation(models.Model):
    """Рекомендация для HR по дальнейшим шагам"""
    
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='hr_recommendations',
        verbose_name=_('Отклик')
    )
    
    recommendation_type = models.CharField(
        max_length=50,
        choices=[
            ('interview', _('Провести собеседование')),
            ('test', _('Назначить тест')),
            ('phone', _('Телефонное интервью')),
            ('reject', _('Отклонить')),
            ('wait', _('Дождаться дополнительных откликов')),
        ],
        verbose_name=_('Тип рекомендации')
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Заголовок')
    )
    
    description = models.TextField(
        verbose_name=_('Описание')
    )
    
    priority = models.CharField(
        max_length=20,
        choices=[
            ('high', _('Высокий')),
            ('medium', _('Средний')),
            ('low', _('Низкий')),
        ],
        default='medium',
        verbose_name=_('Приоритет')
    )
    
    is_completed = models.BooleanField(
        default=False,
        verbose_name=_('Выполнено')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    
    class Meta:
        verbose_name = _('Рекомендация HR')
        verbose_name_plural = _('Рекомендации HR')
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.application.vacancy.title} - {self.title}"
