from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    # Рекомендации для кандидатов
    path('candidate/', views.candidate_recommendations, name='candidate_recommendations'),
    path('search/', views.search_recommendations, name='search_recommendations'),
    path('api/', views.api_recommendations, name='api_recommendations'),
    
    # Рекомендации для HR
    path('hr/<int:vacancy_id>/', views.hr_recommendations, name='hr_recommendations'),
    path('hr/<int:vacancy_id>/refresh/', views.refresh_recommendations, name='refresh_recommendations'),
    
    # Детали рекомендации
    path('details/<int:recommendation_id>/', views.recommendation_details, name='recommendation_details'),
    
    # Анализ файлов резюме
    path('analyze-file/', views.analyze_resume_file, name='analyze_resume_file'),
    path('update-from-file/', views.update_resume_from_file, name='update_resume_from_file'),
]
