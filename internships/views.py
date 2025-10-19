from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Internship, InternshipApplication
from .forms import InternshipForm, InternshipApplicationForm


class InternshipListView(ListView):
    """Список стажировок"""
    model = Internship
    template_name = 'internships/internship_list.html'
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


class InternshipDetailView(DetailView):
    """Детальная страница стажировки"""
    model = Internship
    template_name = 'internships/internship_detail.html'
    context_object_name = 'internship'
    
    def get_queryset(self):
        return Internship.objects.filter(status='published')


@login_required
def apply_to_internship(request, pk):
    """Заявка на стажировку"""
    internship = get_object_or_404(Internship, pk=pk, status='published')
    
    # Проверяем, что пользователь еще не подавал заявку
    if InternshipApplication.objects.filter(internship=internship, company=request.user).exists():
        messages.warning(request, 'Вы уже подавали заявку на эту стажировку.')
        return redirect('internships:detail', pk=pk)
    
    if request.method == 'POST':
        form = InternshipApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.internship = internship
            application.company = request.user
            application.students_count = 1  # Устанавливаем значение по умолчанию
            application.save()
            messages.success(request, 'Ваша заявка успешно отправлена!')
            return redirect('internships:detail', pk=pk)
    else:
        form = InternshipApplicationForm()
    
    return render(request, 'internships/apply.html', {
        'form': form,
        'internship': internship
    })


@login_required
def my_internships(request):
    """Мои стажировки (для представителей вузов)"""
    if not request.user.is_university:
        messages.error(request, 'Доступ запрещен.')
        return redirect('accounts:dashboard')
    
    internships = Internship.objects.filter(university=request.user).order_by('-created_at')
    
    # Фильтрация по статусу
    status = request.GET.get('status')
    if status:
        internships = internships.filter(status=status)
    
    paginator = Paginator(internships, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'internships/my_internships.html', {
        'page_obj': page_obj,
        'status': status
    })


class InternshipCreateView(CreateView):
    """Создание стажировки"""
    model = Internship
    form_class = InternshipForm
    template_name = 'internships/internship_form.html'
    success_url = reverse_lazy('internships:my_internships')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_university:
            messages.error(request, 'Только представители вузов могут создавать стажировки.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.university = self.request.user
        form.instance.status = 'draft'  # Создаем как черновик
        messages.success(self.request, 'Стажировка создана как черновик.')
        return super().form_valid(form)


class InternshipUpdateView(UpdateView):
    """Редактирование стажировки"""
    model = Internship
    form_class = InternshipForm
    template_name = 'internships/internship_form.html'
    success_url = reverse_lazy('internships:my_internships')
    
    def dispatch(self, request, *args, **kwargs):
        internship = self.get_object()
        if internship.university != request.user:
            messages.error(request, 'Вы можете редактировать только свои стажировки.')
            return redirect('internships:my_internships')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Если стажировка была опубликована, после редактирования отправляем на модерацию
        if form.instance.status == 'published':
            form.instance.status = 'pending'
            messages.success(self.request, 'Стажировка обновлена и отправлена на модерацию.')
        else:
            messages.success(self.request, 'Стажировка обновлена.')
        return super().form_valid(form)


@login_required
def internship_applications(request, pk):
    """Заявки на стажировку"""
    internship = get_object_or_404(Internship, pk=pk, university=request.user)
    
    applications = InternshipApplication.objects.filter(internship=internship).order_by('-created_at')
    
    # Фильтрация по статусу
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'internships/internship_applications.html', {
        'internship': internship,
        'page_obj': page_obj,
        'status': status
    })


@login_required
def update_internship_application_status(request, pk):
    """Обновление статуса заявки на стажировку"""
    application = get_object_or_404(InternshipApplication, pk=pk)
    
    if application.internship.university != request.user:
        messages.error(request, 'Доступ запрещен.')
        return redirect('internships:my_internships')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['viewed', 'accepted', 'rejected']:
            application.status = new_status
            application.save()
            messages.success(request, 'Статус заявки обновлен.')
    
    return redirect('internships:applications', pk=application.internship.pk)
