from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Resume, WorkExperience, Education


class ResumeForm(forms.ModelForm):
    """Форма создания/редактирования резюме"""
    
    class Meta:
        model = Resume
        fields = [
            'title', 'summary', 'experience_level', 'education_level',
            'university', 'faculty', 'graduation_year', 'skills', 'languages',
            'salary_expectation', 'is_remote', 'is_relocation', 'resume_file', 'is_public'
        ]
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 5}),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'languages': forms.Textarea(attrs={'rows': 3}),
            'graduation_year': forms.NumberInput(attrs={'min': 1950, 'max': 2030}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        self.fields['resume_file'].widget.attrs.update({
            'accept': '.pdf,.doc,.docx'
        })


class WorkExperienceForm(forms.ModelForm):
    """Форма опыта работы"""
    
    class Meta:
        model = WorkExperience
        fields = ['company', 'position', 'description', 'start_date', 'end_date', 'is_current']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        is_current = cleaned_data.get('is_current')
        
        if not is_current and start_date and end_date and start_date >= end_date:
            raise forms.ValidationError('Дата окончания должна быть позже даты начала.')
        
        return cleaned_data


class EducationForm(forms.ModelForm):
    """Форма образования"""
    
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'start_date', 'end_date', 'is_current']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        is_current = cleaned_data.get('is_current')
        
        if not is_current and start_date and end_date and start_date >= end_date:
            raise forms.ValidationError('Дата окончания должна быть позже даты начала.')
        
        return cleaned_data
