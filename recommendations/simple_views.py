from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from .services import RecommendationService

@login_required
def candidate_recommendations(request):
    """Страница рекомендаций для кандидатов с локальной моделью"""
    if not request.user.is_candidate:
        return render(request, '403.html', status=403)
    
    try:
        # Используем сервис рекомендаций
        service = RecommendationService()
        recommendations = service.get_vacancy_recommendations_for_candidate(request.user)
        
        # Пагинация
        paginator = Paginator(recommendations, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'recommendations': page_obj,
            'total_recommendations': len(recommendations),
            'user': request.user,
            'has_recommendations': len(recommendations) > 0
        }
        
        return render(request, 'recommendations/candidate_recommendations_new.html', context)
        
    except Exception as e:
        # Fallback - показываем пустую страницу с сообщением
        context = {
            'recommendations': [],
            'total_recommendations': 0,
            'user': request.user,
            'has_recommendations': False,
            'error_message': f'Ошибка при получении рекомендаций: {str(e)}'
        }
        return render(request, 'recommendations/candidate_recommendations_new.html', context)

@login_required
def api_recommendations(request):
    """API для получения рекомендаций"""
    if not request.user.is_candidate:
        return JsonResponse({'error': 'Доступ запрещен'}, status=403)
    
    try:
        service = RecommendationService()
        recommendations = service.get_vacancy_recommendations_for_candidate(request.user)
        
        return JsonResponse({
            'success': True,
            'recommendations': recommendations,
            'total': len(recommendations)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка при получении рекомендаций: {str(e)}',
            'recommendations': [],
            'total': 0
        })
