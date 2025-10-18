from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class SkillCategory(models.Model):
    """Категория навыков"""
    
    name = models.CharField(
        max_length=100,
        verbose_name=_('Название категории')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Описание')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    
    class Meta:
        verbose_name = _('Категория навыков')
        verbose_name_plural = _('Категории навыков')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Skill(models.Model):
    """Навык"""
    
    name = models.CharField(
        max_length=100,
        verbose_name=_('Название навыка')
    )
    
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='skills',
        verbose_name=_('Категория')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Описание')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    
    class Meta:
        verbose_name = _('Навык')
        verbose_name_plural = _('Навыки')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"


class SkillTest(models.Model):
    """Тест на навык"""
    
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name=_('Навык')
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Название теста')
    )
    
    description = models.TextField(
        verbose_name=_('Описание теста')
    )
    
    questions = models.TextField(
        verbose_name=_('Вопросы теста'),
        help_text=_('JSON с вопросами и вариантами ответов')
    )
    
    passing_score = models.PositiveIntegerField(
        default=70,
        verbose_name=_('Проходной балл (%)')
    )
    
    time_limit = models.PositiveIntegerField(
        default=30,
        verbose_name=_('Время на прохождение (минуты)')
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Активен')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    
    class Meta:
        verbose_name = _('Тест навыка')
        verbose_name_plural = _('Тесты навыков')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.skill.name}"


class SkillTestResult(models.Model):
    """Результат прохождения теста"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='skill_test_results',
        verbose_name=_('Пользователь')
    )
    
    test = models.ForeignKey(
        SkillTest,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name=_('Тест')
    )
    
    score = models.PositiveIntegerField(
        verbose_name=_('Балл')
    )
    
    max_score = models.PositiveIntegerField(
        verbose_name=_('Максимальный балл')
    )
    
    percentage = models.FloatField(
        verbose_name=_('Процент')
    )
    
    passed = models.BooleanField(
        verbose_name=_('Пройден')
    )
    
    answers = models.TextField(
        verbose_name=_('Ответы пользователя')
    )
    
    completed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата прохождения')
    )
    
    class Meta:
        verbose_name = _('Результат теста')
        verbose_name_plural = _('Результаты тестов')
        ordering = ['-completed_at']
        unique_together = ['user', 'test']
    
    def __str__(self):
        return f"{self.user.email} - {self.test.title} ({self.percentage}%)"
