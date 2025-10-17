from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView
from vacancies.models import Vacancy
from internships.models import Internship


class IndexView(ListView):
    """Главная страница"""
    template_name = 'catalog/index.html'
    context_object_name = 'recent_vacancies'
    
    def get_queryset(self):
        return Vacancy.objects.filter(status='published').order_by('-published_at')[:6]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_internships'] = Internship.objects.filter(status='published').order_by('-published_at')[:6]
        return context


class PublicVacancyListView(ListView):
    """Публичный список вакансий"""
    model = Vacancy
    template_name = 'catalog/vacancy_list.html'
    context_object_name = 'vacancies'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Vacancy.objects.filter(status='published')
        
        # Фильтрация по поиску
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(company__company__icontains=search)
            )
        
        # Фильтрация по опыту
        experience = self.request.GET.get('experience')
        if experience:
            queryset = queryset.filter(experience_level=experience)
        
        # Фильтрация по удаленной работе
        remote = self.request.GET.get('remote')
        if remote == 'true':
            queryset = queryset.filter(is_remote=True)
        
        return queryset.order_by('-published_at')


class PublicInternshipListView(ListView):
    """Публичный список стажировок"""
    model = Internship
    template_name = 'catalog/internship_list.html'
    context_object_name = 'internships'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Internship.objects.filter(status='published')
        
        # Фильтрация по поиску
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(specialization__icontains=search) |
                Q(university__company__icontains=search)
            )
        
        # Фильтрация по специальности
        specialization = self.request.GET.get('specialization')
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        
        # Фильтрация по продолжительности
        duration = self.request.GET.get('duration')
        if duration:
            queryset = queryset.filter(duration=duration)
        
        # Фильтрация по удаленной работе
        remote = self.request.GET.get('remote')
        if remote == 'true':
            queryset = queryset.filter(is_remote=True)
        
        return queryset.order_by('-published_at')


def about(request):
    """Страница о платформе"""
    return render(request, 'catalog/about.html')


def contact(request):
    """Страница контактов"""
    return render(request, 'catalog/contact.html')
