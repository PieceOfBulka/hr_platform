from django.urls import path
from . import views

app_name = 'internships'

urlpatterns = [
    path('', views.InternshipListView.as_view(), name='list'),
    path('<int:pk>/', views.InternshipDetailView.as_view(), name='detail'),
    path('<int:pk>/apply/', views.apply_to_internship, name='apply'),
    path('my/', views.my_internships, name='my_internships'),
    path('create/', views.InternshipCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.InternshipUpdateView.as_view(), name='update'),
    path('<int:pk>/applications/', views.internship_applications, name='applications'),
    path('applications/<int:pk>/update-status/', views.update_internship_application_status, name='update_application_status'),
]
