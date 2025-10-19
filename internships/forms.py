from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Internship, PracticeRequest, InternshipApplication, PracticeApplication


class InternshipForm(forms.ModelForm):
    """Форма создания/редактирования стажировки"""
    
    class Meta:
        model = Internship
        fields = [
            'title', 'description', 'requirements', 'tasks',
            'specialization', 'duration',
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


class PracticeRequestForm(forms.ModelForm):
    """Форма создания/редактирования заявки на практику"""
    
    class Meta:
        model = PracticeRequest
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
            'status': forms.Select(choices=PracticeRequest.Status.choices),
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
    """Форма отклика на стажировку для авторизованных пользователей"""
    
    add_to_public_bank = forms.BooleanField(
        required=False,
        initial=True,
        label='Разместить резюме в общем банке',
        help_text='Позволит другим HR-менеджерам увидеть ваше резюме'
    )
    
    class Meta:
        model = InternshipApplication
        fields = ['cover_letter', 'resume_file']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Расскажите о себе и почему вы подходите для этой стажировки...'}),
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


class AnonymousInternshipApplicationForm(forms.ModelForm):
    """Форма отклика на стажировку для неавторизованных пользователей"""
    
    class Meta:
        model = InternshipApplication
        fields = ['candidate_name', 'candidate_email', 'candidate_phone', 'cover_letter', 'resume_file']
        widgets = {
            'candidate_name': forms.TextInput(attrs={'placeholder': 'Ваше имя и фамилия'}),
            'candidate_email': forms.EmailInput(attrs={'placeholder': 'your.email@example.com'}),
            'candidate_phone': forms.TextInput(attrs={'placeholder': '+7 (999) 123-45-67'}),
            'cover_letter': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Расскажите о себе и почему вы подходите для этой стажировки...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget.__class__.__name__ != 'CheckboxInput':
                field.widget.attrs.update({'class': 'form-control'})
        
        # Делаем поля обязательными
        self.fields['candidate_name'].required = True
        self.fields['candidate_email'].required = True
        self.fields['candidate_phone'].required = True
        
        self.fields['resume_file'].widget.attrs.update({
            'accept': '.pdf,.doc,.docx'
        })


class PracticeApplicationForm(forms.ModelForm):
    """Форма отклика HR на заявку вуза на практику"""
    
    class Meta:
        model = PracticeApplication
        fields = ['message', 'students_count']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Расскажите о вашей компании и возможностях для студентов...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        self.fields['students_count'].widget.attrs.update({
            'min': 1,
            'max': 50
        })
