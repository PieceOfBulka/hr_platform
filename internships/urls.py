from django.urls import path
from . import views

app_name = 'internships'

urlpatterns = [
    # Стажировки
    path('', views.InternshipListView.as_view(), name='list'),
    path('<int:pk>/', views.InternshipDetailView.as_view(), name='detail'),
    path('<int:pk>/apply/', views.apply_to_internship, name='apply'),
    path('my/', views.my_internships, name='my_internships'),
    path('create/', views.InternshipCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.InternshipUpdateView.as_view(), name='update'),
    path('<int:pk>/applications/', views.internship_applications, name='applications'),
    path('applications/<int:pk>/update-status/', views.update_internship_application_status, name='update_application_status'),
    
    # Заявки на практику
    path('practice/', views.PracticeRequestListView.as_view(), name='practice_list'),
    path('practice/<int:pk>/', views.PracticeRequestDetailView.as_view(), name='practice_detail'),
    path('practice/<int:pk>/apply/', views.apply_to_practice_request, name='apply_practice'),
    path('practice/my/', views.my_practice_requests, name='my_practice_requests'),
    path('practice/create/', views.PracticeRequestCreateView.as_view(), name='create_practice'),
    path('practice/<int:pk>/edit/', views.PracticeRequestUpdateView.as_view(), name='update_practice'),
    path('practice/<int:pk>/applications/', views.practice_request_applications, name='practice_applications'),
    path('practice/applications/<int:pk>/update-status/', views.update_practice_application_status, name='update_practice_application_status'),
]
