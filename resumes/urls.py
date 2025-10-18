from django.urls import path
from . import views

app_name = 'resumes'

urlpatterns = [
    path('', views.ResumeListView.as_view(), name='list'),
    path('<int:pk>/', views.ResumeDetailView.as_view(), name='detail'),
    path('my/', views.my_resume, name='my_resume'),
    path('create/', views.ResumeCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.ResumeUpdateView.as_view(), name='update'),
    path('<int:pk>/add-experience/', views.work_experience_create, name='add_experience'),
    path('<int:pk>/add-education/', views.education_create, name='add_education'),
    path('work-experience/create/', views.work_experience_create, name='work_experience_create'),
    path('work-experience/<int:pk>/edit/', views.work_experience_update, name='work_experience_update'),
    path('work-experience/<int:pk>/delete/', views.work_experience_delete, name='work_experience_delete'),
    path('education/create/', views.education_create, name='education_create'),
    path('education/<int:pk>/edit/', views.education_update, name='education_update'),
    path('education/<int:pk>/delete/', views.education_delete, name='education_delete'),
]
