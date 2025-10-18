from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Internship, InternshipApplication


class InternshipForm(forms.ModelForm):
    """Форма создания/редактирования стажировки"""
    
    class Meta:
        model = Internship
        fields = [
            'title', 'description', 'requirements', 'tasks',
            'specialization', 'students_count', 'duration',
            'start_date', 'end_date', 'contact_email', 'contact_phone', 'is_remote', 'status'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'tasks': forms.Textarea(attrs={'rows': 5}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=Internship.Status.choices),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError('Дата окончания должна быть позже даты начала.')
        
        return cleaned_data


class InternshipApplicationForm(forms.ModelForm):
    """Форма заявки на стажировку"""
    
    class Meta:
        model = InternshipApplication
        fields = ['message', 'students_count']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Расскажите о вашей компании и возможностях для стажеров...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        self.fields['students_count'].widget.attrs.update({
            'min': '1',
            'max': '50'
        })
