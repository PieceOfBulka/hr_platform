from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import User
from .forms import CustomUserCreationForm, UserUpdateForm


class CustomLoginView(LoginView):
    """Кастомный вход в систему"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')


class CustomLogoutView(LogoutView):
    """Выход из системы"""
    next_page = reverse_lazy('catalog:index')


class SignUpView(CreateView):
    """Регистрация нового пользователя"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Регистрация прошла успешно! Ожидайте подтверждения администратора.')
        return super().form_valid(form)


@login_required
def dashboard(request):
    """Личный кабинет пользователя"""
    user = request.user
    
    context = {
        'user': user,
    }
    
    # В зависимости от роли показываем разный контент
    if user.is_admin:
        template = 'accounts/admin_dashboard.html'
    elif user.is_hr:
        template = 'accounts/hr_dashboard.html'
    elif user.is_university:
        template = 'accounts/university_dashboard.html'
    else:
        template = 'accounts/candidate_dashboard.html'
    
    return render(request, template, context)


class ProfileUpdateView(UpdateView):
    """Обновление профиля пользователя"""
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:dashboard')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)
