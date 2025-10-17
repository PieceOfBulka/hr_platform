from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView
from django.utils import timezone
from vacancies.models import Vacancy
from internships.models import Internship
from accounts.models import User


@login_required
def moderation_dashboard(request):
    """Панель модерации"""
    if not request.user.is_admin:
        messages.error(request, 'Доступ запрещен.')
        return redirect('accounts:dashboard')
    
    # Статистика
    pending_vacancies = Vacancy.objects.filter(status='pending').count()
    pending_internships = Internship.objects.filter(status='pending').count()
    total_users = User.objects.count()
    new_users_today = User.objects.filter(created_at__date=timezone.now().date()).count()
    
    context = {
        'pending_vacancies': pending_vacancies,
        'pending_internships': pending_internships,
        'total_users': total_users,
        'new_users_today': new_users_today,
    }
    
    return render(request, 'moderation/dashboard.html', context)


class VacancyModerationListView(ListView):
    """Список вакансий на модерации"""
    model = Vacancy
    template_name = 'moderation/vacancy_list.html'
    context_object_name = 'vacancies'
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'Доступ запрещен.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        status = self.request.GET.get('status', 'pending')
        return Vacancy.objects.filter(status=status).order_by('-created_at')


@login_required
def vacancy_moderate(request, pk):
    """Модерация вакансии"""
    if not request.user.is_admin:
        messages.error(request, 'Доступ запрещен.')
        return redirect('accounts:dashboard')
    
    vacancy = get_object_or_404(Vacancy, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        comment = request.POST.get('comment', '')
        
        if action == 'approve':
            vacancy.status = 'published'
            vacancy.published_at = timezone.now()
            vacancy.save()
            messages.success(request, 'Вакансия одобрена и опубликована.')
        elif action == 'reject':
            vacancy.status = 'rejected'
            vacancy.save()
            messages.success(request, 'Вакансия отклонена.')
        
        return redirect('moderation:vacancies')
    
    return render(request, 'moderation/vacancy_moderate.html', {
        'vacancy': vacancy
    })


class InternshipModerationListView(ListView):
    """Список стажировок на модерации"""
    model = Internship
    template_name = 'moderation/internship_list.html'
    context_object_name = 'internships'
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'Доступ запрещен.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        status = self.request.GET.get('status', 'pending')
        return Internship.objects.filter(status=status).order_by('-created_at')


@login_required
def internship_moderate(request, pk):
    """Модерация стажировки"""
    if not request.user.is_admin:
        messages.error(request, 'Доступ запрещен.')
        return redirect('accounts:dashboard')
    
    internship = get_object_or_404(Internship, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        comment = request.POST.get('comment', '')
        
        if action == 'approve':
            internship.status = 'published'
            internship.published_at = timezone.now()
            internship.save()
            messages.success(request, 'Стажировка одобрена и опубликована.')
        elif action == 'reject':
            internship.status = 'rejected'
            internship.save()
            messages.success(request, 'Стажировка отклонена.')
        
        return redirect('moderation:internships')
    
    return render(request, 'moderation/internship_moderate.html', {
        'internship': internship
    })


class UserModerationListView(ListView):
    """Список пользователей для модерации"""
    model = User
    template_name = 'moderation/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'Доступ запрещен.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = User.objects.all()
        
        # Фильтрация по роли
        role = self.request.GET.get('role')
        if role:
            queryset = queryset.filter(role=role)
        
        # Фильтрация по статусу верификации
        verified = self.request.GET.get('verified')
        if verified == 'true':
            queryset = queryset.filter(is_verified=True)
        elif verified == 'false':
            queryset = queryset.filter(is_verified=False)
        
        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(company__icontains=search)
            )
        
        return queryset.order_by('-created_at')


@login_required
def user_moderate(request, pk):
    """Модерация пользователя"""
    if not request.user.is_admin:
        messages.error(request, 'Доступ запрещен.')
        return redirect('accounts:dashboard')
    
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'verify':
            user.is_verified = True
            user.save()
            messages.success(request, 'Пользователь верифицирован.')
        elif action == 'unverify':
            user.is_verified = False
            user.save()
            messages.success(request, 'Верификация пользователя отменена.')
        elif action == 'activate':
            user.is_active = True
            user.save()
            messages.success(request, 'Пользователь активирован.')
        elif action == 'deactivate':
            user.is_active = False
            user.save()
            messages.success(request, 'Пользователь деактивирован.')
        
        return redirect('moderation:users')
    
    return render(request, 'moderation/user_moderate.html', {
        'user': user
    })


@login_required
def statistics(request):
    """Статистика платформы"""
    if not request.user.is_admin:
        messages.error(request, 'Доступ запрещен.')
        return redirect('accounts:dashboard')
    
    # Общая статистика
    total_vacancies = Vacancy.objects.count()
    published_vacancies = Vacancy.objects.filter(status='published').count()
    pending_vacancies = Vacancy.objects.filter(status='pending').count()
    
    total_internships = Internship.objects.count()
    published_internships = Internship.objects.filter(status='published').count()
    pending_internships = Internship.objects.filter(status='pending').count()
    
    total_users = User.objects.count()
    verified_users = User.objects.filter(is_verified=True).count()
    
    # Статистика по ролям
    users_by_role = {}
    for role, display in User.Role.choices:
        users_by_role[display] = User.objects.filter(role=role).count()
    
    # Статистика по компаниям
    companies = User.objects.filter(role=User.Role.HR).values_list('company', flat=True).distinct()
    companies_count = len([c for c in companies if c])
    
    context = {
        'total_vacancies': total_vacancies,
        'published_vacancies': published_vacancies,
        'pending_vacancies': pending_vacancies,
        'total_internships': total_internships,
        'published_internships': published_internships,
        'pending_internships': pending_internships,
        'total_users': total_users,
        'verified_users': verified_users,
        'users_by_role': users_by_role,
        'companies_count': companies_count,
    }
    
    return render(request, 'moderation/statistics.html', context)
