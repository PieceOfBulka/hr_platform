from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def candidate_recommendations(request):
    """Простая страница рекомендаций для кандидатов"""
    if not request.user.is_candidate:
        return render(request, '403.html', status=403)
    
    # Пока что показываем заглушку
    context = {
        'recommendations': [],
        'total_recommendations': 0,
        'user': request.user
    }
    
    return render(request, 'recommendations/candidate_recommendations.html', context)

@login_required
def api_recommendations(request):
    """API для получения рекомендаций"""
    if not request.user.is_candidate:
        return JsonResponse({'error': 'Доступ запрещен'}, status=403)
    
    # Пока что возвращаем пустой список
    return JsonResponse({
        'success': True,
        'recommendations': [],
        'total': 0
    })
