from django.contrib import admin
from .models import Internship, InternshipApplication


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    """Админка для стажировок"""
    
    list_display = ('title', 'university', 'status', 'specialization', 'students_count', 'start_date', 'end_date')
    list_filter = ('status', 'specialization', 'is_remote', 'created_at')
    search_fields = ('title', 'description', 'university__company')
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'requirements', 'tasks')
        }),
        ('Детали стажировки', {
            'fields': ('specialization', 'students_count', 'duration', 'start_date', 'end_date', 'is_remote')
        }),
        ('Контакты', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Статус', {
            'fields': ('status', 'university', 'published_at')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    """Админка для заявок на стажировки"""
    
    list_display = ('internship', 'company', 'status', 'students_count', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('internship__title', 'company__company', 'message')
    readonly_fields = ('created_at',)
