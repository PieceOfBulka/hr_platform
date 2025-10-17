from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('vacancies/', views.PublicVacancyListView.as_view(), name='vacancies'),
    path('internships/', views.PublicInternshipListView.as_view(), name='internships'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
