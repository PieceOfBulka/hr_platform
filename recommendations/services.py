from django.db.models import Q
from django.core.cache import cache
from django.conf import settings
import requests
import json
import logging
from typing import List, Dict, Tuple, Optional, Any
from vacancies.models import Vacancy, Application
from resumes.models import Resume
from .models import RecommendationRule, ResumeRecommendation, HRRecommendation
from .resume_parser import ResumeAnalyzer

logger = logging.getLogger(__name__)


class GemmaRecommendationService:
    """Сервис рекомендаций на основе Gemma LLM"""
    
    def __init__(self):
        self.api_token = getattr(settings, 'HUGGINGFACE_API_TOKEN', None)
        self.api_url = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def analyze_resume_vacancy_match(self, resume: Resume, vacancy: Vacancy) -> Dict:
        """Анализирует соответствие резюме и вакансии с помощью LLM"""
        try:
            # Подготавливаем данные для анализа
            resume_data = {
                'title': resume.title,
                'summary': resume.summary or '',
                'skills': resume.skills or '',
                'experience_level': resume.experience_level,
                'education_level': resume.education_level,
                'salary_expectation': resume.salary_expectation,
                'is_remote': resume.is_remote
            }
            
            vacancy_data = {
                'title': vacancy.title,
                'description': vacancy.description,
                'requirements': vacancy.requirements,
                'experience_level': vacancy.experience_level,
                'salary_min': vacancy.salary_min,
                'salary_max': vacancy.salary_max,
                'is_remote': vacancy.is_remote
            }
            
            # Формируем промпт для LLM
            prompt = self._create_analysis_prompt(resume_data, vacancy_data)
            
            # Отправляем запрос к API
            response = self._call_gemma_api(prompt)
            
            if response:
                return self._parse_llm_response(response)
            else:
                return self._fallback_analysis(resume_data, vacancy_data)
                
        except Exception as e:
            logger.error(f"Ошибка при анализе LLM: {e}")
            return self._fallback_analysis(resume_data, vacancy_data)
    
    def _create_analysis_prompt(self, resume_data: Dict, vacancy_data: Dict) -> str:
        """Создает промпт для анализа соответствия"""
        return f"""
Проанализируй соответствие кандидата и вакансии. Оцени по шкале от 0 до 10 и объясни причины.

КАНДИДАТ:
- Желаемая должность: {resume_data['title']}
- О себе: {resume_data['summary']}
- Навыки: {resume_data['skills']}
- Уровень опыта: {resume_data['experience_level']}
- Образование: {resume_data['education_level']}
- Желаемая зарплата: {resume_data['salary_expectation']}
- Готов к удаленной работе: {resume_data['is_remote']}

ВАКАНСИЯ:
- Должность: {vacancy_data['title']}
- Описание: {vacancy_data['description']}
- Требования: {vacancy_data['requirements']}
- Требуемый опыт: {vacancy_data['experience_level']}
- Зарплата: {vacancy_data['salary_min']}-{vacancy_data['salary_max']}
- Удаленная работа: {vacancy_data['is_remote']}

Ответь в формате JSON:
{{
    "score": число_от_0_до_10,
    "match_reasons": ["причина1", "причина2"],
    "mismatch_reasons": ["несоответствие1", "несоответствие2"],
    "recommendations": ["рекомендация1", "рекомендация2"]
}}
"""
    
    def _call_gemma_api(self, prompt: str) -> Optional[Dict]:
        """Вызывает API Gemma"""
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 512,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Ошибка API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Ошибка при вызове API: {e}")
            return None
    
    def _parse_llm_response(self, response: Dict) -> Dict:
        """Парсит ответ от LLM"""
        try:
            if isinstance(response, list) and len(response) > 0:
                text = response[0].get('generated_text', '')
            else:
                text = str(response)
            
            # Пытаемся извлечь JSON из ответа
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # Если JSON не найден, используем fallback
                return self._extract_score_from_text(text)
                
        except Exception as e:
            logger.error(f"Ошибка при парсинге ответа LLM: {e}")
            return self._extract_score_from_text(str(response))
    
    def _extract_score_from_text(self, text: str) -> Dict:
        """Извлекает оценку из текстового ответа"""
        import re
        
        # Ищем число от 0 до 10
        score_match = re.search(r'(\d+(?:\.\d+)?)', text)
        score = float(score_match.group(1)) if score_match else 5.0
        
        return {
            "score": min(max(score, 0), 10),
            "match_reasons": ["Анализ LLM"],
            "mismatch_reasons": [],
            "recommendations": ["Рассмотреть кандидата"]
        }
    
    def _fallback_analysis(self, resume_data: Dict, vacancy_data: Dict) -> Dict:
        """Fallback анализ без LLM"""
        score = 5.0
        match_reasons = []
        mismatch_reasons = []
        
        # Простая логика сопоставления
        if resume_data['title'].lower() in vacancy_data['title'].lower():
            score += 2.0
            match_reasons.append("Совпадение должности")
        
        if resume_data['skills'] and vacancy_data['requirements']:
            skills_lower = resume_data['skills'].lower()
            req_lower = vacancy_data['requirements'].lower()
            if any(skill in req_lower for skill in skills_lower.split(',')):
                score += 1.5
                match_reasons.append("Совпадение навыков")
        
        return {
            "score": min(max(score, 0), 10),
            "match_reasons": match_reasons,
            "mismatch_reasons": mismatch_reasons,
            "recommendations": ["Базовый анализ"]
        }


class RecommendationService:
    """Улучшенный сервис рекомендаций с LLM"""
    
    def __init__(self):
        self.gemma_service = GemmaRecommendationService()
        self.resume_analyzer = ResumeAnalyzer()
    
    def calculate_resume_score(self, resume: Resume, vacancy: Vacancy) -> Tuple[float, List[Dict]]:
        """Вычисляет оценку совпадения резюме с вакансией с использованием LLM"""
        # Проверяем кэш
        cache_key = f"recommendation_{resume.id}_{vacancy.id}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result['score'], cached_result['matched_rules']
        
        # Анализируем с помощью LLM
        llm_analysis = self.gemma_service.analyze_resume_vacancy_match(resume, vacancy)
        
        # Дополняем традиционным анализом
        traditional_score, traditional_rules = self._calculate_traditional_score(resume, vacancy)
        
        # Комбинируем результаты
        final_score = (llm_analysis['score'] * 0.7 + traditional_score * 0.3)
        matched_rules = self._combine_analysis_results(llm_analysis, traditional_rules)
        
        # Кэшируем результат
        cache.set(cache_key, {
            'score': final_score,
            'matched_rules': matched_rules
        }, 3600 * 24)  # 24 часа
        
        return final_score, matched_rules
    
    def _calculate_traditional_score(self, resume: Resume, vacancy: Vacancy) -> Tuple[float, List[Dict]]:
        """Традиционный расчет оценки без LLM"""
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
    
    def _combine_analysis_results(self, llm_analysis: Dict, traditional_rules: List[Dict]) -> List[Dict]:
        """Объединяет результаты LLM и традиционного анализа"""
        combined_rules = []
        
        # Добавляем результаты LLM
        if llm_analysis.get('match_reasons'):
            combined_rules.append({
                'rule': 'LLM Analysis',
                'score': llm_analysis['score'] * 0.1,
                'reasons': llm_analysis['match_reasons']
            })
        
        # Добавляем традиционные правила
        combined_rules.extend(traditional_rules)
        
        return combined_rules
    
    def analyze_resume_file(self, resume_file_path: str) -> Dict[str, Any]:
        """Анализирует файл резюме и извлекает структурированную информацию"""
        try:
            analysis = self.resume_analyzer.analyze_resume_file(resume_file_path)
            return analysis
        except Exception as e:
            logger.error(f"Ошибка при анализе файла резюме {resume_file_path}: {e}")
            return {}
    
    def extract_skills_from_file(self, resume_file_path: str) -> List[str]:
        """Извлекает навыки из файла резюме"""
        try:
            analysis = self.analyze_resume_file(resume_file_path)
            return analysis.get('parsed_data', {}).get('skills', [])
        except Exception as e:
            logger.error(f"Ошибка при извлечении навыков из файла: {e}")
            return []
    
    def update_resume_from_file(self, resume: Resume, resume_file_path: str) -> bool:
        """Обновляет резюме на основе анализа файла"""
        try:
            analysis = self.analyze_resume_file(resume_file_path)
            parsed_data = analysis.get('parsed_data', {})
            
            if not parsed_data:
                return False
            
            # Обновляем поля резюме
            if parsed_data.get('skills'):
                current_skills = resume.skills or ''
                new_skills = ', '.join(parsed_data['skills'])
                resume.skills = f"{current_skills}, {new_skills}".strip(', ')
            
            if parsed_data.get('summary'):
                resume.summary = parsed_data['summary']
            
            if parsed_data.get('experience_years'):
                years = parsed_data['experience_years']
                if years == 0:
                    resume.experience_level = Resume.ExperienceLevel.NO_EXPERIENCE
                elif years <= 2:
                    resume.experience_level = Resume.ExperienceLevel.JUNIOR
                elif years <= 5:
                    resume.experience_level = Resume.ExperienceLevel.MIDDLE
                elif years <= 8:
                    resume.experience_level = Resume.ExperienceLevel.SENIOR
                else:
                    resume.experience_level = Resume.ExperienceLevel.LEAD
            
            if parsed_data.get('education_level'):
                education_mapping = {
                    'secondary': Resume.EducationLevel.SECONDARY,
                    'bachelor': Resume.EducationLevel.BACHELOR,
                    'master': Resume.EducationLevel.MASTER,
                    'phd': Resume.EducationLevel.PHD,
                    'doctor': Resume.EducationLevel.DOCTOR,
                }
                resume.education_level = education_mapping.get(
                    parsed_data['education_level'], 
                    Resume.EducationLevel.BACHELOR
                )
            
            resume.save()
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при обновлении резюме из файла: {e}")
            return False
    
    def generate_resume_recommendations(self, vacancy: Vacancy) -> List[ResumeRecommendation]:
        """Генерирует рекомендации резюме для вакансии с использованием LLM"""
        # Получаем все публичные резюме
        resumes = Resume.objects.filter(is_public=True)
        
        # Удаляем существующие рекомендации для этой вакансии
        ResumeRecommendation.objects.filter(vacancy=vacancy).delete()
        
        recommendations = []
        service = RecommendationService()
        
        for resume in resumes:
            score, matched_rules = service.calculate_resume_score(resume, vacancy)
            
            if score > 3.0:  # Минимальный порог для рекомендации
                recommendation = ResumeRecommendation.objects.create(
                    vacancy=vacancy,
                    resume=resume,
                    score=score,
                    matched_rules=json.dumps(matched_rules, ensure_ascii=False)
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    def get_vacancy_recommendations_for_candidate(self, candidate: 'User') -> List[Dict]:
        """Получает рекомендации вакансий для конкретного кандидата"""
        try:
            resume = candidate.resume
            if not resume:
                return []
            
            # Получаем все опубликованные вакансии
            vacancies = Vacancy.objects.filter(status='published')
            
            recommendations = []
            service = RecommendationService()
            
            for vacancy in vacancies:
                score, matched_rules = service.calculate_resume_score(resume, vacancy)
                
                if score > 3.0:  # Минимальный порог
                    recommendations.append({
                        'vacancy': vacancy,
                        'score': score,
                        'matched_rules': matched_rules,
                        'match_percentage': min(score * 10, 100)
                    })
            
            # Сортируем по оценке
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            return recommendations[:10]  # Топ-10 рекомендаций
            
        except Exception as e:
            logger.error(f"Ошибка при получении рекомендаций для кандидата: {e}")
            return []
    
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
