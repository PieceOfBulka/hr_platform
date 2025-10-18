from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админка для пользователей"""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'company', 'is_verified', 'is_active')
    list_filter = ('role', 'is_verified', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Дополнительная информация'), {
            'fields': ('role', 'phone', 'company', 'position', 'is_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Дополнительная информация'), {
            'fields': ('role', 'phone', 'company', 'position', 'is_verified')
        }),
    )
