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
            'contact_email', 'contact_phone', 'is_remote', 'auto_close_date', 'status'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'responsibilities': forms.Textarea(attrs={'rows': 5}),
            'auto_close_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'status': forms.Select(choices=Vacancy.Status.choices),
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
    
    add_to_public_bank = forms.BooleanField(
        required=False,
        initial=True,
        label='Разместить резюме в общем банке',
        help_text='Позволит другим HR-менеджерам увидеть ваше резюме'
    )
    
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume_file']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Расскажите о себе и почему вы подходите для этой позиции...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget.__class__.__name__ != 'CheckboxInput':
                field.widget.attrs.update({'class': 'form-control'})
        
        self.fields['resume_file'].widget.attrs.update({
            'accept': '.pdf,.doc,.docx'
        })
        
        self.fields['add_to_public_bank'].widget.attrs.update({
            'class': 'form-check-input'
        })
