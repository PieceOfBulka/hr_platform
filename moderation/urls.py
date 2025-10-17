from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('', views.moderation_dashboard, name='dashboard'),
    path('vacancies/', views.VacancyModerationListView.as_view(), name='vacancies'),
    path('vacancies/<int:pk>/moderate/', views.vacancy_moderate, name='vacancy_moderate'),
    path('internships/', views.InternshipModerationListView.as_view(), name='internships'),
    path('internships/<int:pk>/moderate/', views.internship_moderate, name='internship_moderate'),
    path('users/', views.UserModerationListView.as_view(), name='users'),
    path('users/<int:pk>/moderate/', views.user_moderate, name='user_moderate'),
    path('statistics/', views.statistics, name='statistics'),
]
