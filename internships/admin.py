from django.contrib import admin
from .models import Internship, InternshipApplication


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    """Админка для стажировок"""
    
    list_display = ('title', 'type', 'organization', 'status', 'specialization', 'start_date', 'end_date')
    list_filter = ('type', 'status', 'specialization', 'is_remote', 'created_at')
    search_fields = ('title', 'description', 'organization__company')
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('type', 'title', 'description', 'requirements', 'tasks')
        }),
        ('Детали стажировки/практики', {
            'fields': ('specialization', 'duration', 'start_date', 'end_date', 'is_remote')
        }),
        ('Контакты', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Статус', {
            'fields': ('status', 'organization', 'published_at')
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
