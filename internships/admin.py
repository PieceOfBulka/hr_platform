from django.contrib import admin
from .models import Internship, PracticeRequest, InternshipApplication, PracticeApplication


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    """Админка для стажировок"""
    
    list_display = ('title', 'company', 'status', 'specialization', 'start_date', 'end_date')
    list_filter = ('status', 'specialization', 'is_remote', 'created_at')
    search_fields = ('title', 'description', 'company__company')
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'requirements', 'tasks')
        }),
        ('Детали стажировки', {
            'fields': ('specialization', 'duration', 'start_date', 'end_date', 'is_remote')
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


@admin.register(PracticeRequest)
class PracticeRequestAdmin(admin.ModelAdmin):
    """Админка для заявок на практику"""
    
    list_display = ('title', 'university', 'status', 'specialization', 'students_count', 'start_date', 'end_date')
    list_filter = ('status', 'specialization', 'is_remote', 'created_at')
    search_fields = ('title', 'description', 'university__company')
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'requirements', 'tasks')
        }),
        ('Детали практики', {
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
    """Админка для откликов на стажировки"""
    
    list_display = ('internship', 'candidate', 'candidate_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('internship__title', 'candidate__email', 'candidate_name', 'candidate_email')
    readonly_fields = ('created_at',)


@admin.register(PracticeApplication)
class PracticeApplicationAdmin(admin.ModelAdmin):
    """Админка для откликов HR на заявки практики"""
    
    list_display = ('practice_request', 'hr_company', 'status', 'students_count', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('practice_request__title', 'hr_company__company')
    readonly_fields = ('created_at',)
