from django.contrib import admin
from .models import Vacancy, Application


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """Админка для вакансий"""
    
    list_display = ('title', 'company', 'status', 'experience_level', 'salary_min', 'salary_max', 'created_at')
    list_filter = ('status', 'experience_level', 'is_remote', 'created_at')
    search_fields = ('title', 'description', 'company__company')
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'requirements', 'responsibilities')
        }),
        ('Условия работы', {
            'fields': ('salary_min', 'salary_max', 'experience_level', 'is_remote', 'auto_close_date')
        }),
        ('Контакты', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Статус', {
            'fields': ('status', 'company', 'published_at')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Админка для откликов"""
    
    list_display = ('vacancy', 'candidate', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('vacancy__title', 'candidate__email', 'cover_letter')
    readonly_fields = ('created_at',)
