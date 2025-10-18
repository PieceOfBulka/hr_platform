from django.contrib import admin
from .models import RecommendationRule, ResumeRecommendation, HRRecommendation


@admin.register(RecommendationRule)
class RecommendationRuleAdmin(admin.ModelAdmin):
    """Админка для правил рекомендаций"""
    
    list_display = ('name', 'skill_keywords', 'experience_level', 'weight', 'is_active', 'created_at')
    list_filter = ('is_active', 'experience_level', 'is_remote', 'created_at')
    search_fields = ('name', 'description', 'skill_keywords')
    readonly_fields = ('created_at',)


@admin.register(ResumeRecommendation)
class ResumeRecommendationAdmin(admin.ModelAdmin):
    """Админка для рекомендаций резюме"""
    
    list_display = ('vacancy', 'resume', 'score', 'created_at')
    list_filter = ('created_at', 'vacancy__company')
    search_fields = ('vacancy__title', 'resume__title', 'resume__user__email')
    readonly_fields = ('created_at',)


@admin.register(HRRecommendation)
class HRRecommendationAdmin(admin.ModelAdmin):
    """Админка для рекомендаций HR"""
    
    list_display = ('application', 'recommendation_type', 'title', 'priority', 'is_completed', 'created_at')
    list_filter = ('recommendation_type', 'priority', 'is_completed', 'created_at')
    search_fields = ('title', 'description', 'application__vacancy__title')
    readonly_fields = ('created_at',)
