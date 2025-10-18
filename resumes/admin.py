from django.contrib import admin
from .models import Resume, WorkExperience, Education


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """Админка для резюме"""
    
    list_display = ('title', 'user', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('title', 'summary', 'skills', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'summary', 'skills')
        }),
        ('Настройки', {
            'fields': ('is_public', 'user')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    """Админка для опыта работы"""
    
    list_display = ('position', 'company', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current', 'start_date')
    search_fields = ('position', 'company', 'description')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    """Админка для образования"""
    
    list_display = ('institution', 'degree', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current', 'start_date')
    search_fields = ('institution', 'degree')
