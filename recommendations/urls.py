from django.urls import path
from . import simple_views as views

app_name = 'recommendations'

urlpatterns = [
    # Рекомендации для кандидатов
    path('candidate/', views.candidate_recommendations, name='candidate_recommendations'),
    path('api/', views.api_recommendations, name='api_recommendations'),
]
