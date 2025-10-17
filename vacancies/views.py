from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Vacancy, Application
from .forms import VacancyForm, ApplicationForm


class VacancyListView(ListView):
    """Список вакансий"""
    model = Vacancy
    template_name = 'vacancies/vacancy_list.html'
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


class VacancyDetailView(DetailView):
    """Детальная страница вакансии"""
    model = Vacancy
    template_name = 'vacancies/vacancy_detail.html'
    context_object_name = 'vacancy'
    
    def get_queryset(self):
        return Vacancy.objects.filter(status='published')


@login_required
def apply_to_vacancy(request, pk):
    """Отклик на вакансию"""
    vacancy = get_object_or_404(Vacancy, pk=pk, status='published')
    
    # Проверяем, что пользователь - соискатель
    if not request.user.is_candidate:
        messages.error(request, 'Только соискатели могут откликаться на вакансии.')
        return redirect('vacancies:detail', pk=pk)
    
    # Проверяем, что пользователь еще не откликался
    if Application.objects.filter(vacancy=vacancy, candidate=request.user).exists():
        messages.warning(request, 'Вы уже откликались на эту вакансию.')
        return redirect('vacancies:detail', pk=pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.vacancy = vacancy
            application.candidate = request.user
            application.save()
            messages.success(request, 'Ваш отклик успешно отправлен!')
            return redirect('vacancies:detail', pk=pk)
    else:
        form = ApplicationForm()
    
    return render(request, 'vacancies/apply.html', {
        'form': form,
        'vacancy': vacancy
    })


@login_required
def my_vacancies(request):
    """Мои вакансии (для HR)"""
    if not request.user.is_hr:
        messages.error(request, 'Доступ запрещен.')
        return redirect('accounts:dashboard')
    
    vacancies = Vacancy.objects.filter(company=request.user).order_by('-created_at')
    
    # Фильтрация по статусу
    status = request.GET.get('status')
    if status:
        vacancies = vacancies.filter(status=status)
    
    paginator = Paginator(vacancies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'vacancies/my_vacancies.html', {
        'page_obj': page_obj,
        'status': status
    })


class VacancyCreateView(CreateView):
    """Создание вакансии"""
    model = Vacancy
    form_class = VacancyForm
    template_name = 'vacancies/vacancy_form.html'
    success_url = reverse_lazy('vacancies:my_vacancies')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_hr:
            messages.error(request, 'Только HR могут создавать вакансии.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.company = self.request.user
        form.instance.status = 'pending'  # Отправляем на модерацию
        messages.success(self.request, 'Вакансия создана и отправлена на модерацию.')
        return super().form_valid(form)


class VacancyUpdateView(UpdateView):
    """Редактирование вакансии"""
    model = Vacancy
    form_class = VacancyForm
    template_name = 'vacancies/vacancy_form.html'
    success_url = reverse_lazy('vacancies:my_vacancies')
    
    def dispatch(self, request, *args, **kwargs):
        vacancy = self.get_object()
        if vacancy.company != request.user:
            messages.error(request, 'Вы можете редактировать только свои вакансии.')
            return redirect('vacancies:my_vacancies')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Если вакансия была опубликована, после редактирования отправляем на модерацию
        if form.instance.status == 'published':
            form.instance.status = 'pending'
            messages.success(self.request, 'Вакансия обновлена и отправлена на модерацию.')
        else:
            messages.success(self.request, 'Вакансия обновлена.')
        return super().form_valid(form)


@login_required
def vacancy_applications(request, pk):
    """Отклики на вакансию"""
    vacancy = get_object_or_404(Vacancy, pk=pk, company=request.user)
    
    applications = Application.objects.filter(vacancy=vacancy).order_by('-created_at')
    
    # Фильтрация по статусу
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'vacancies/vacancy_applications.html', {
        'vacancy': vacancy,
        'page_obj': page_obj,
        'status': status
    })


@login_required
def update_application_status(request, pk):
    """Обновление статуса отклика"""
    application = get_object_or_404(Application, pk=pk)
    
    if application.vacancy.company != request.user:
        messages.error(request, 'Доступ запрещен.')
        return redirect('vacancies:my_vacancies')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['viewed', 'interview', 'accepted', 'rejected']:
            application.status = new_status
            application.save()
            messages.success(request, 'Статус отклика обновлен.')
    
    return redirect('vacancies:applications', pk=application.vacancy.pk)
