from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Resume, WorkExperience, Education
from .forms import ResumeForm, WorkExperienceForm, EducationForm


@login_required
def my_resume(request):
    """Мое резюме"""
    if not request.user.is_candidate:
        messages.error(request, 'Доступ запрещен.')
        return redirect('accounts:dashboard')
    
    try:
        resume = request.user.resume
    except Resume.DoesNotExist:
        return redirect('resumes:create')
    
    return render(request, 'resumes/my_resume.html', {
        'resume': resume
    })


class ResumeCreateView(CreateView):
    """Создание резюме"""
    model = Resume
    form_class = ResumeForm
    template_name = 'resumes/resume_form.html'
    success_url = reverse_lazy('resumes:my_resume')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_candidate:
            messages.error(request, 'Только соискатели могут создавать резюме.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Резюме создано успешно!')
        return super().form_valid(form)


class ResumeUpdateView(UpdateView):
    """Редактирование резюме"""
    model = Resume
    form_class = ResumeForm
    template_name = 'resumes/resume_form.html'
    success_url = reverse_lazy('resumes:my_resume')
    
    def dispatch(self, request, *args, **kwargs):
        resume = self.get_object()
        if resume.user != request.user:
            messages.error(request, 'Вы можете редактировать только свое резюме.')
            return redirect('resumes:my_resume')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Резюме обновлено успешно!')
        return super().form_valid(form)


class ResumeListView(ListView):
    """Список публичных резюме (для HR)"""
    model = Resume
    template_name = 'resumes/resume_list.html'
    context_object_name = 'resumes'
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_hr:
            messages.error(request, 'Доступ запрещен.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Resume.objects.filter(is_public=True)
        
        # Фильтрация по поиску
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(skills__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )
        
        # Фильтрация по уровню опыта
        experience = self.request.GET.get('experience')
        if experience:
            queryset = queryset.filter(experience_level=experience)
        
        # Фильтрация по готовности к удаленной работе
        remote = self.request.GET.get('remote')
        if remote == 'true':
            queryset = queryset.filter(is_remote=True)
        
        return queryset.order_by('-updated_at')


class ResumeDetailView(DetailView):
    """Детальная страница резюме"""
    model = Resume
    template_name = 'resumes/resume_detail.html'
    context_object_name = 'resume'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_hr:
            messages.error(request, 'Доступ запрещен.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_public:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Резюме не доступно для просмотра")
        return obj


@login_required
def work_experience_create(request):
    """Добавление опыта работы"""
    if not request.user.is_candidate:
        messages.error(request, 'Доступ запрещен.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            work_exp = form.save(commit=False)
            work_exp.resume = request.user.resume
            work_exp.save()
            messages.success(request, 'Опыт работы добавлен!')
            return redirect('resumes:my_resume')
    else:
        form = WorkExperienceForm()
    
    return render(request, 'resumes/work_experience_form.html', {
        'form': form,
        'title': 'Добавить опыт работы'
    })


@login_required
def work_experience_update(request, pk):
    """Редактирование опыта работы"""
    work_exp = get_object_or_404(WorkExperience, pk=pk, resume__user=request.user)
    
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST, instance=work_exp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Опыт работы обновлен!')
            return redirect('resumes:my_resume')
    else:
        form = WorkExperienceForm(instance=work_exp)
    
    return render(request, 'resumes/work_experience_form.html', {
        'form': form,
        'title': 'Редактировать опыт работы'
    })


@login_required
def work_experience_delete(request, pk):
    """Удаление опыта работы"""
    work_exp = get_object_or_404(WorkExperience, pk=pk, resume__user=request.user)
    
    if request.method == 'POST':
        work_exp.delete()
        messages.success(request, 'Опыт работы удален!')
        return redirect('resumes:my_resume')
    
    return render(request, 'resumes/work_experience_confirm_delete.html', {
        'work_exp': work_exp
    })


@login_required
def education_create(request):
    """Добавление образования"""
    if not request.user.is_candidate:
        messages.error(request, 'Доступ запрещен.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.resume = request.user.resume
            education.save()
            messages.success(request, 'Образование добавлено!')
            return redirect('resumes:my_resume')
    else:
        form = EducationForm()
    
    return render(request, 'resumes/education_form.html', {
        'form': form,
        'title': 'Добавить образование'
    })


@login_required
def education_update(request, pk):
    """Редактирование образования"""
    education = get_object_or_404(Education, pk=pk, resume__user=request.user)
    
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, 'Образование обновлено!')
            return redirect('resumes:my_resume')
    else:
        form = EducationForm(instance=education)
    
    return render(request, 'resumes/education_form.html', {
        'form': form,
        'title': 'Редактировать образование'
    })


@login_required
def education_delete(request, pk):
    """Удаление образования"""
    education = get_object_or_404(Education, pk=pk, resume__user=request.user)
    
    if request.method == 'POST':
        education.delete()
        messages.success(request, 'Образование удалено!')
        return redirect('resumes:my_resume')
    
    return render(request, 'resumes/education_confirm_delete.html', {
        'education': education
    })
