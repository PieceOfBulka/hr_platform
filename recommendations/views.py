from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import tempfile

from .services import RecommendationService
from .models import ResumeRecommendation, HRRecommendation
from vacancies.models import Vacancy
from resumes.models import Resume

User = get_user_model()


@login_required
def candidate_recommendations(request):
    """Страница с рекомендациями вакансий для кандидата"""
    if not request.user.is_candidate:
        return render(request, '403.html', status=403)
    
    try:
        service = RecommendationService()
        recommendations = service.get_vacancy_recommendations_for_candidate(request.user)
        
        # Пагинация
        paginator = Paginator(recommendations, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'recommendations': page_obj,
            'total_recommendations': len(recommendations),
            'user': request.user
        }
        
        return render(request, 'recommendations/candidate_recommendations.html', context)
        
    except Exception as e:
        return render(request, 'recommendations/error.html', {
            'error_message': f'Ошибка при получении рекомендаций: {str(e)}'
        })


@login_required
def hr_recommendations(request, vacancy_id):
    """Страница с рекомендациями резюме для HR"""
    if not request.user.is_hr:
        return render(request, '403.html', status=403)
    
    vacancy = get_object_or_404(Vacancy, id=vacancy_id, company=request.user)
    
    try:
        service = RecommendationService()
        recommendations = service.generate_resume_recommendations(vacancy)
        
        # Пагинация
        paginator = Paginator(recommendations, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'vacancy': vacancy,
            'recommendations': page_obj,
            'total_recommendations': len(recommendations)
        }
        
        return render(request, 'recommendations/hr_recommendations.html', context)
        
    except Exception as e:
        return render(request, 'recommendations/error.html', {
            'error_message': f'Ошибка при получении рекомендаций: {str(e)}'
        })


@login_required
@require_http_methods(["POST"])
def refresh_recommendations(request, vacancy_id):
    """Обновляет рекомендации для вакансии"""
    if not request.user.is_hr:
        return JsonResponse({'error': 'Доступ запрещен'}, status=403)
    
    vacancy = get_object_or_404(Vacancy, id=vacancy_id, company=request.user)
    
    try:
        service = RecommendationService()
        recommendations = service.generate_resume_recommendations(vacancy)
        
        return JsonResponse({
            'success': True,
            'message': f'Обновлено {len(recommendations)} рекомендаций',
            'count': len(recommendations)
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Ошибка при обновлении рекомендаций: {str(e)}'
        }, status=500)


@login_required
def recommendation_details(request, recommendation_id):
    """Детальная информация о рекомендации"""
    recommendation = get_object_or_404(ResumeRecommendation, id=recommendation_id)
    
    # Проверяем права доступа
    if request.user.is_candidate and recommendation.resume.user != request.user:
        return render(request, '403.html', status=403)
    elif request.user.is_hr and recommendation.vacancy.company != request.user:
        return render(request, '403.html', status=403)
    
    context = {
        'recommendation': recommendation,
        'vacancy': recommendation.vacancy,
        'resume': recommendation.resume,
        'matched_rules': recommendation.matched_rules if isinstance(recommendation.matched_rules, list) else []
    }
    
    return render(request, 'recommendations/recommendation_details.html', context)


@login_required
def api_recommendations(request):
    """API для получения рекомендаций"""
    if not request.user.is_candidate:
        return JsonResponse({'error': 'Доступ запрещен'}, status=403)
    
    try:
        service = RecommendationService()
        recommendations = service.get_vacancy_recommendations_for_candidate(request.user)
        
        # Преобразуем в JSON-совместимый формат
        recommendations_data = []
        for rec in recommendations:
            recommendations_data.append({
                'vacancy_id': rec['vacancy'].id,
                'vacancy_title': rec['vacancy'].title,
                'company': rec['vacancy'].company.company,
                'score': rec['score'],
                'match_percentage': rec['match_percentage'],
                'description': rec['vacancy'].description[:200] + '...' if len(rec['vacancy'].description) > 200 else rec['vacancy'].description,
                'salary_min': rec['vacancy'].salary_min,
                'salary_max': rec['vacancy'].salary_max,
                'is_remote': rec['vacancy'].is_remote,
                'matched_rules': rec['matched_rules']
            })
        
        return JsonResponse({
            'success': True,
            'recommendations': recommendations_data,
            'total': len(recommendations_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Ошибка при получении рекомендаций: {str(e)}'
        }, status=500)


@login_required
def search_recommendations(request):
    """Поиск рекомендаций с фильтрами"""
    if not request.user.is_candidate:
        return render(request, '403.html', status=403)
    
    # Получаем параметры поиска
    search_query = request.GET.get('q', '')
    experience_level = request.GET.get('experience', '')
    salary_min = request.GET.get('salary_min', '')
    salary_max = request.GET.get('salary_max', '')
    is_remote = request.GET.get('remote', '')
    
    try:
        service = RecommendationService()
        recommendations = service.get_vacancy_recommendations_for_candidate(request.user)
        
        # Применяем фильтры
        filtered_recommendations = []
        for rec in recommendations:
            vacancy = rec['vacancy']
            
            # Фильтр по тексту
            if search_query:
                if not any(search_query.lower() in field.lower() for field in [
                    vacancy.title, vacancy.description, vacancy.requirements
                ]):
                    continue
            
            # Фильтр по опыту
            if experience_level and vacancy.experience_level != experience_level:
                continue
            
            # Фильтр по зарплате
            if salary_min and vacancy.salary_min and vacancy.salary_min < int(salary_min):
                continue
            if salary_max and vacancy.salary_max and vacancy.salary_max > int(salary_max):
                continue
            
            # Фильтр по удаленной работе
            if is_remote and vacancy.is_remote != (is_remote == 'true'):
                continue
            
            filtered_recommendations.append(rec)
        
        # Пагинация
        paginator = Paginator(filtered_recommendations, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'recommendations': page_obj,
            'total_recommendations': len(filtered_recommendations),
            'search_query': search_query,
            'experience_level': experience_level,
            'salary_min': salary_min,
            'salary_max': salary_max,
            'is_remote': is_remote,
            'user': request.user
        }
        
        return render(request, 'recommendations/search_recommendations.html', context)
        
    except Exception as e:
        return render(request, 'recommendations/error.html', {
            'error_message': f'Ошибка при поиске рекомендаций: {str(e)}'
        })


@login_required
@require_http_methods(["POST"])
def analyze_resume_file(request):
    """Анализирует загруженный файл резюме"""
    if not request.user.is_candidate:
        return JsonResponse({'error': 'Доступ запрещен'}, status=403)
    
    if 'resume_file' not in request.FILES:
        return JsonResponse({'error': 'Файл не найден'}, status=400)
    
    try:
        uploaded_file = request.FILES['resume_file']
        
        # Проверяем тип файла
        allowed_extensions = ['.pdf', '.docx', '.txt']
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            return JsonResponse({
                'error': f'Неподдерживаемый формат файла. Разрешены: {", ".join(allowed_extensions)}'
            }, status=400)
        
        # Сохраняем временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        # Анализируем файл
        service = RecommendationService()
        analysis = service.analyze_resume_file(temp_file_path)
        
        # Удаляем временный файл
        os.unlink(temp_file_path)
        
        if not analysis:
            return JsonResponse({'error': 'Не удалось проанализировать файл'}, status=400)
        
        # Возвращаем результаты анализа
        parsed_data = analysis.get('parsed_data', {})
        
        return JsonResponse({
            'success': True,
            'analysis': {
                'full_name': parsed_data.get('full_name'),
                'email': parsed_data.get('email'),
                'phone': parsed_data.get('phone'),
                'skills': parsed_data.get('skills', []),
                'experience_years': parsed_data.get('experience_years'),
                'education_level': parsed_data.get('education_level'),
                'languages': parsed_data.get('languages', []),
                'summary': parsed_data.get('summary'),
                'work_experience': parsed_data.get('work_experience', []),
                'education': parsed_data.get('education', [])
            },
            'scores': {
                'skill_score': analysis.get('skill_score', 0),
                'experience_level': analysis.get('experience_level', 'no_experience'),
                'education_score': analysis.get('education_score', 0),
                'completeness_score': analysis.get('completeness_score', 0)
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Ошибка при анализе файла: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["POST"])
def update_resume_from_file(request):
    """Обновляет резюме пользователя на основе анализа файла"""
    if not request.user.is_candidate:
        return JsonResponse({'error': 'Доступ запрещен'}, status=403)
    
    if 'resume_file' not in request.FILES:
        return JsonResponse({'error': 'Файл не найден'}, status=400)
    
    try:
        # Получаем или создаем резюме пользователя
        resume, created = Resume.objects.get_or_create(
            user=request.user,
            defaults={
                'title': 'Резюме',
                'summary': '',
                'skills': '',
                'experience_level': Resume.ExperienceLevel.JUNIOR,
                'education_level': Resume.EducationLevel.BACHELOR,
            }
        )
        
        uploaded_file = request.FILES['resume_file']
        
        # Сохраняем файл резюме
        resume.resume_file = uploaded_file
        resume.save()
        
        # Анализируем файл и обновляем резюме
        service = RecommendationService()
        
        # Создаем временный файл для анализа
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        # Обновляем резюме на основе анализа
        success = service.update_resume_from_file(resume, temp_file_path)
        
        # Удаляем временный файл
        os.unlink(temp_file_path)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Резюме успешно обновлено на основе анализа файла',
                'resume': {
                    'title': resume.title,
                    'summary': resume.summary,
                    'skills': resume.skills,
                    'experience_level': resume.get_experience_level_display(),
                    'education_level': resume.get_education_level_display(),
                }
            })
        else:
            return JsonResponse({
                'error': 'Не удалось обновить резюме на основе файла'
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'error': f'Ошибка при обновлении резюме: {str(e)}'
        }, status=500)
