from django.contrib import admin
from .models import SkillCategory, Skill, SkillTest, SkillTestResult


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    """Админка для категорий навыков"""
    
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Админка для навыков"""
    
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')


@admin.register(SkillTest)
class SkillTestAdmin(admin.ModelAdmin):
    """Админка для тестов навыков"""
    
    list_display = ('title', 'skill', 'passing_score', 'time_limit', 'is_active', 'created_at')
    list_filter = ('skill__category', 'is_active', 'created_at')
    search_fields = ('title', 'skill__name')
    readonly_fields = ('created_at',)


@admin.register(SkillTestResult)
class SkillTestResultAdmin(admin.ModelAdmin):
    """Админка для результатов тестов"""
    
    list_display = ('user', 'test', 'score', 'percentage', 'passed', 'completed_at')
    list_filter = ('passed', 'test__skill__category', 'completed_at')
    search_fields = ('user__email', 'test__title')
    readonly_fields = ('completed_at',)
