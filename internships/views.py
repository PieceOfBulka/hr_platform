from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Internship, PracticeRequest, InternshipApplication, PracticeApplication
from .forms import InternshipForm, PracticeRequestForm, InternshipApplicationForm, AnonymousInternshipApplicationForm, PracticeApplicationForm


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
                Q(company__company__icontains=search)
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


class PracticeRequestListView(ListView):
    """Список заявок на практику"""
    model = PracticeRequest
    template_name = 'internships/practice_request_list.html'
    context_object_name = 'practice_requests'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = PracticeRequest.objects.filter(status='published')
        
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


class PracticeRequestDetailView(DetailView):
    """Детальная страница заявки на практику"""
    model = PracticeRequest
    template_name = 'internships/practice_request_detail.html'
    context_object_name = 'practice_request'
    
    def get_queryset(self):
        return PracticeRequest.objects.filter(status='published')


def apply_to_internship(request, pk):
    """Отклик на стажировку (для соискателей)"""
    internship = get_object_or_404(Internship, pk=pk, status='published')
    
    if request.user.is_authenticated:
        # Проверяем, что пользователь еще не откликался
        if InternshipApplication.objects.filter(internship=internship, candidate=request.user).exists():
            messages.warning(request, 'Вы уже откликались на эту стажировку.')
            return redirect('internships:detail', pk=pk)
        
        if request.method == 'POST':
            form = InternshipApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                application = form.save(commit=False)
                application.internship = internship
                application.candidate = request.user
                application.save()
                
                # Если пользователь выбрал размещение в общем банке
                if form.cleaned_data.get('add_to_public_bank'):
                    # Создаем или обновляем резюме пользователя
                    from resumes.models import Resume
                    resume, created = Resume.objects.get_or_create(
                        user=request.user,
                        defaults={
                            'title': f'Резюме {request.user.get_full_name() or request.user.email}',
                            'summary': application.cover_letter,
                            'is_public': True
                        }
                    )
                    if not created:
                        resume.is_public = True
                        resume.save()
                
                messages.success(request, 'Ваш отклик успешно отправлен!')
                return redirect('internships:detail', pk=pk)
        else:
            form = InternshipApplicationForm()
    else:
        # Анонимный отклик
        if request.method == 'POST':
            form = AnonymousInternshipApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                application = form.save(commit=False)
                application.internship = internship
                application.save()
                messages.success(request, 'Ваш отклик успешно отправлен!')
                return redirect('internships:detail', pk=pk)
        else:
            form = AnonymousInternshipApplicationForm()
    
    return render(request, 'internships/apply.html', {
        'form': form,
        'internship': internship
    })


@login_required
def apply_to_practice_request(request, pk):
    """Отклик HR на заявку вуза на практику"""
    practice_request = get_object_or_404(PracticeRequest, pk=pk, status='published')
    
    if not request.user.is_hr:
        messages.error(request, 'Только HR могут откликаться на заявки практики.')
        return redirect('internships:practice_detail', pk=pk)
    
    # Проверяем, что HR еще не откликался
    if PracticeApplication.objects.filter(practice_request=practice_request, hr_company=request.user).exists():
        messages.warning(request, 'Вы уже откликались на эту заявку практики.')
        return redirect('internships:practice_detail', pk=pk)
    
    if request.method == 'POST':
        form = PracticeApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.practice_request = practice_request
            application.hr_company = request.user
            application.save()
            messages.success(request, 'Ваш отклик успешно отправлен!')
            return redirect('internships:practice_detail', pk=pk)
    else:
        form = PracticeApplicationForm()
    
    return render(request, 'internships/apply_practice.html', {
        'form': form,
        'practice_request': practice_request
    })


@login_required
def my_internships(request):
    """Мои стажировки (для HR)"""
    if not request.user.is_hr:
        messages.error(request, 'Доступ запрещен.')
        return redirect('accounts:dashboard')
    
    internships = Internship.objects.filter(company=request.user).order_by('-created_at')
    
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


@login_required
def my_practice_requests(request):
    """Мои заявки на практику (для представителей вузов)"""
    if not request.user.is_university:
        messages.error(request, 'Доступ запрещен.')
        return redirect('accounts:dashboard')
    
    practice_requests = PracticeRequest.objects.filter(university=request.user).order_by('-created_at')
    
    # Фильтрация по статусу
    status = request.GET.get('status')
    if status:
        practice_requests = practice_requests.filter(status=status)
    
    paginator = Paginator(practice_requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'internships/my_practice_requests.html', {
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
        if not request.user.is_hr:
            messages.error(request, 'Только HR могут создавать стажировки.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.company = self.request.user
        form.instance.status = 'draft'  # Создаем как черновик
        messages.success(self.request, 'Стажировка создана как черновик.')
        return super().form_valid(form)


class PracticeRequestCreateView(CreateView):
    """Создание заявки на практику"""
    model = PracticeRequest
    form_class = PracticeRequestForm
    template_name = 'internships/practice_request_form.html'
    success_url = reverse_lazy('internships:my_practice_requests')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_university:
            messages.error(request, 'Только представители вузов могут создавать заявки на практику.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.university = self.request.user
        form.instance.status = 'draft'  # Создаем как черновик
        messages.success(self.request, 'Заявка на практику создана как черновик.')
        return super().form_valid(form)


class InternshipUpdateView(UpdateView):
    """Редактирование стажировки"""
    model = Internship
    form_class = InternshipForm
    template_name = 'internships/internship_form.html'
    success_url = reverse_lazy('internships:my_internships')
    
    def dispatch(self, request, *args, **kwargs):
        internship = self.get_object()
        if internship.company != request.user:
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


class PracticeRequestUpdateView(UpdateView):
    """Редактирование заявки на практику"""
    model = PracticeRequest
    form_class = PracticeRequestForm
    template_name = 'internships/practice_request_form.html'
    success_url = reverse_lazy('internships:my_practice_requests')
    
    def dispatch(self, request, *args, **kwargs):
        practice_request = self.get_object()
        if practice_request.university != request.user:
            messages.error(request, 'Вы можете редактировать только свои заявки на практику.')
            return redirect('internships:my_practice_requests')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Если заявка была опубликована, после редактирования отправляем на модерацию
        if form.instance.status == 'published':
            form.instance.status = 'pending'
            messages.success(self.request, 'Заявка на практику обновлена и отправлена на модерацию.')
        else:
            messages.success(self.request, 'Заявка на практику обновлена.')
        return super().form_valid(form)


@login_required
def internship_applications(request, pk):
    """Отклики на стажировку"""
    internship = get_object_or_404(Internship, pk=pk, company=request.user)
    
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
def practice_request_applications(request, pk):
    """Отклики HR на заявку практики"""
    practice_request = get_object_or_404(PracticeRequest, pk=pk, university=request.user)
    
    applications = PracticeApplication.objects.filter(practice_request=practice_request).order_by('-created_at')
    
    # Фильтрация по статусу
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'internships/practice_request_applications.html', {
        'practice_request': practice_request,
        'page_obj': page_obj,
        'status': status
    })


@login_required
def update_internship_application_status(request, pk):
    """Обновление статуса отклика на стажировку"""
    application = get_object_or_404(InternshipApplication, pk=pk)
    
    if application.internship.company != request.user:
        messages.error(request, 'Доступ запрещен.')
        return redirect('internships:my_internships')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['viewed', 'interview', 'accepted', 'rejected']:
            application.status = new_status
            application.save()
            messages.success(request, 'Статус отклика обновлен.')
    
    return redirect('internships:applications', pk=application.internship.pk)


@login_required
def update_practice_application_status(request, pk):
    """Обновление статуса отклика HR на заявку практики"""
    application = get_object_or_404(PracticeApplication, pk=pk)
    
    if application.practice_request.university != request.user:
        messages.error(request, 'Доступ запрещен.')
        return redirect('internships:my_practice_requests')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['viewed', 'accepted', 'rejected']:
            application.status = new_status
            application.save()
            messages.success(request, 'Статус отклика обновлен.')
    
    return redirect('internships:practice_applications', pk=application.practice_request.pk)
