from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'company', 'position')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget = forms.Select(choices=User.Role.choices)
        self.fields['role'].help_text = 'Выберите вашу роль в системе'
        
        # Добавляем Bootstrap классы
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class UserUpdateForm(forms.ModelForm):
    """Форма обновления профиля пользователя"""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'company', 'position')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
