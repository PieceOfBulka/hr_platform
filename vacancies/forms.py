from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Vacancy, Application


class VacancyForm(forms.ModelForm):
    """Форма создания/редактирования вакансии"""
    
    class Meta:
        model = Vacancy
        fields = [
            'title', 'description', 'requirements', 'responsibilities',
            'salary_min', 'salary_max', 'experience_level',
            'contact_email', 'contact_phone', 'is_remote', 'auto_close_date'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'responsibilities': forms.Textarea(attrs={'rows': 5}),
            'auto_close_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        self.fields['auto_close_date'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Необязательно'
        })


class ApplicationForm(forms.ModelForm):
    """Форма отклика на вакансию"""
    
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume_file']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Расскажите о себе и почему вы подходите для этой позиции...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        self.fields['resume_file'].widget.attrs.update({
            'accept': '.pdf,.doc,.docx'
        })
