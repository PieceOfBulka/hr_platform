from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Расширенная модель пользователя с ролями"""
    
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Администратор ОЭЗ')
        HR = 'hr', _('HR компании')
        UNIVERSITY = 'university', _('Представитель вуза')
        CANDIDATE = 'candidate', _('Соискатель')
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CANDIDATE,
        verbose_name=_('Роль')
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Телефон')
    )
    
    company = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Компания/Организация')
    )
    
    position = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Должность')
    )
    
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('Верифицирован')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_role_display(self):
        return dict(self.Role.choices)[self.role]
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_hr(self):
        return self.role == self.Role.HR
    
    @property
    def is_university(self):
        return self.role == self.Role.UNIVERSITY
    
    @property
    def is_candidate(self):
        return self.role == self.Role.CANDIDATE
