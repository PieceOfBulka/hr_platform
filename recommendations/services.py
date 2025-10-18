from django.db.models import Q
from vacancies.models import Vacancy, Application
from resumes.models import Resume
from .models import RecommendationRule, ResumeRecommendation, HRRecommendation


class RecommendationService:
    """Сервис рекомендаций"""
    
    @staticmethod
    def calculate_resume_score(resume, vacancy):
        """Вычисляет оценку совпадения резюме с вакансией"""
        score = 0.0
        matched_rules = []
        
        # Получаем активные правила
        rules = RecommendationRule.objects.filter(is_active=True)
        
        for rule in rules:
            rule_score = 0.0
            
            # Проверка навыков
            if rule.skill_keywords:
                keywords = [kw.strip().lower() for kw in rule.skill_keywords.split(',')]
                resume_skills = resume.skills.lower() if resume.skills else ''
                resume_summary = resume.summary.lower() if resume.summary else ''
                
                for keyword in keywords:
                    if keyword in resume_skills or keyword in resume_summary:
                        rule_score += 1.0
                
                if rule_score > 0:
                    rule_score = min(rule_score / len(keywords), 1.0)
            
            # Проверка уровня опыта
            if rule.experience_level:
                # Здесь можно добавить логику сопоставления опыта
                # Пока просто добавляем базовую оценку
                rule_score += 0.3
            
            # Проверка зарплаты
            if rule.salary_min and rule.salary_max:
                if resume.salary_expectation:
                    if rule.salary_min <= resume.salary_expectation <= rule.salary_max:
                        rule_score += 0.5
            
            # Проверка удаленной работы
            if rule.is_remote is not None:
                if resume.is_remote == rule.is_remote:
                    rule_score += 0.2
            
            if rule_score > 0:
                final_rule_score = rule_score * rule.weight
                score += final_rule_score
                matched_rules.append({
                    'rule': rule.name,
                    'score': final_rule_score
                })
        
        return min(score, 10.0), matched_rules
    
    @staticmethod
    def generate_resume_recommendations(vacancy):
        """Генерирует рекомендации резюме для вакансии"""
        # Получаем все публичные резюме
        resumes = Resume.objects.filter(is_public=True)
        
        # Удаляем существующие рекомендации для этой вакансии
        ResumeRecommendation.objects.filter(vacancy=vacancy).delete()
        
        recommendations = []
        for resume in resumes:
            score, matched_rules = RecommendationService.calculate_resume_score(resume, vacancy)
            
            if score > 3.0:  # Минимальный порог для рекомендации
                recommendation = ResumeRecommendation.objects.create(
                    vacancy=vacancy,
                    resume=resume,
                    score=score,
                    matched_rules=matched_rules
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    @staticmethod
    def generate_hr_recommendations(application):
        """Генерирует рекомендации для HR по отклику"""
        vacancy = application.vacancy
        candidate = application.candidate
        
        # Удаляем существующие рекомендации для этого отклика
        HRRecommendation.objects.filter(application=application).delete()
        
        recommendations = []
        
        # Анализируем отклик
        cover_letter = application.cover_letter.lower() if application.cover_letter else ''
        
        # Рекомендация на основе качества сопроводительного письма
        if len(cover_letter) > 100:
            recommendations.append(HRRecommendation.objects.create(
                application=application,
                recommendation_type='interview',
                title='Качественное сопроводительное письмо',
                description='Кандидат написал подробное сопроводительное письмо. Рекомендуется провести собеседование.',
                priority='high'
            ))
        elif len(cover_letter) > 50:
            recommendations.append(HRRecommendation.objects.create(
                application=application,
                recommendation_type='phone',
                title='Краткое сопроводительное письмо',
                description='Сопроводительное письмо короткое. Рекомендуется телефонное интервью для уточнения деталей.',
                priority='medium'
            ))
        else:
            recommendations.append(HRRecommendation.objects.create(
                application=application,
                recommendation_type='test',
                title='Минимальное сопроводительное письмо',
                description='Сопроводительное письмо очень краткое. Рекомендуется назначить тест для оценки навыков.',
                priority='medium'
            ))
        
        # Рекомендация на основе количества откликов на вакансию
        total_applications = vacancy.applications.count()
        if total_applications > 10:
            recommendations.append(HRRecommendation.objects.create(
                application=application,
                recommendation_type='wait',
                title='Много откликов на вакансию',
                description=f'На вакансию уже {total_applications} откликов. Рекомендуется дождаться дополнительных кандидатов.',
                priority='low'
            ))
        elif total_applications < 3:
            recommendations.append(HRRecommendation.objects.create(
                application=application,
                recommendation_type='interview',
                title='Мало откликов на вакансию',
                description=f'На вакансию всего {total_applications} откликов. Рекомендуется рассмотреть всех кандидатов.',
                priority='high'
            ))
        
        # Рекомендация на основе навыков (если есть резюме)
        try:
            resume = candidate.resume
            if resume and resume.skills:
                skills = resume.skills.lower()
                vacancy_requirements = vacancy.requirements.lower() if vacancy.requirements else ''
                
                # Простая проверка совпадения навыков
                skill_matches = 0
                if 'python' in vacancy_requirements and 'python' in skills:
                    skill_matches += 1
                if 'javascript' in vacancy_requirements and 'javascript' in skills:
                    skill_matches += 1
                if 'react' in vacancy_requirements and 'react' in skills:
                    skill_matches += 1
                
                if skill_matches > 0:
                    recommendations.append(HRRecommendation.objects.create(
                        application=application,
                        recommendation_type='interview',
                        title='Совпадение навыков',
                        description=f'Найдено {skill_matches} совпадений навыков. Рекомендуется собеседование.',
                        priority='high'
                    ))
        except Resume.DoesNotExist:
            pass
        
        return recommendations
