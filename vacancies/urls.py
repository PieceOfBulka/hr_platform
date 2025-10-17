from django.urls import path
from . import views

app_name = 'vacancies'

urlpatterns = [
    path('', views.VacancyListView.as_view(), name='list'),
    path('<int:pk>/', views.VacancyDetailView.as_view(), name='detail'),
    path('<int:pk>/apply/', views.apply_to_vacancy, name='apply'),
    path('my/', views.my_vacancies, name='my_vacancies'),
    path('create/', views.VacancyCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.VacancyUpdateView.as_view(), name='update'),
    path('<int:pk>/applications/', views.vacancy_applications, name='applications'),
    path('applications/<int:pk>/update-status/', views.update_application_status, name='update_application_status'),
]
