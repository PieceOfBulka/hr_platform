from sqlalchemy.orm import Session
from database import Resume, Vacancy, ListOfSkills, Recommendation, Application
from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from datetime import datetime, timedelta

class RecommendationEngine:
    def __init__(self, db: Session):
        self.db = db
        self.vectorizer = TfidfVectorizer(
            stop_words=None,
            ngram_range=(1, 2),
            max_features=1000
        )
    
    def calculate_skill_match_score(self, resume_skills: List[int], vacancy_skills: List[int], 
                                  required_skills: List[int]) -> float:
        """
        Рассчитывает оценку совпадения навыков между резюме и вакансией
        """
        if not vacancy_skills:
            return 0.0
        
        # Навыки резюме
        resume_skill_set = set(resume_skills)
        vacancy_skill_set = set(vacancy_skills)
        required_skill_set = set(required_skills)
        
        # Общие навыки
        common_skills = resume_skill_set.intersection(vacancy_skill_set)
        
        # Обязательные навыки, которые есть у кандидата
        required_skills_met = resume_skill_set.intersection(required_skill_set)
        
        # Базовый скор на основе общих навыков
        skill_match_score = len(common_skills) / len(vacancy_skill_set)
        
        # Бонус за обязательные навыки
        if required_skill_set:
            required_bonus = len(required_skills_met) / len(required_skill_set) * 0.3
            skill_match_score += required_bonus
        
        return min(skill_match_score, 1.0)
    
    def calculate_experience_score(self, resume_experience: int, vacancy_requirements: str) -> float:
        """
        Рассчитывает оценку соответствия опыта работы
        """
        if not vacancy_requirements:
            return 0.5  # Нейтральная оценка если нет требований
        
        # Извлекаем требования к опыту из текста
        experience_patterns = [
            r'(\d+)\+?\s*(?:лет|года|год|years?)',
            r'от\s*(\d+)\s*(?:лет|года|год)',
            r'(\d+)\s*-\s*(\d+)\s*(?:лет|года|год)'
        ]
        
        min_experience = 0
        max_experience = 10
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, vacancy_requirements.lower())
            if matches:
                if isinstance(matches[0], tuple):
                    min_exp, max_exp = matches[0]
                    min_experience = int(min_exp)
                    max_experience = int(max_exp)
                else:
                    min_experience = int(matches[0])
                    max_experience = min_experience + 2
        
        # Рассчитываем соответствие опыта
        if resume_experience >= min_experience:
            if max_experience > min_experience:
                if resume_experience <= max_experience:
                    return 1.0  # Идеальное соответствие
                else:
                    return 0.8  # Больше требуемого, но хорошо
            else:
                return 1.0  # Соответствует минимальным требованиям
        else:
            # Недостаточно опыта
            return max(0.0, resume_experience / min_experience)
    
    def calculate_text_similarity(self, resume_text: str, vacancy_text: str) -> float:
        """
        Рассчитывает текстовое сходство между резюме и вакансией
        """
        if not resume_text or not vacancy_text:
            return 0.0
        
        try:
            # Объединяем тексты для обучения векторизатора
            texts = [resume_text, vacancy_text]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Рассчитываем косинусное сходство
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            return 0.0
    
    def calculate_specialty_match(self, resume_specialty: str, vacancy_title: str, 
                                vacancy_description: str) -> float:
        """
        Рассчитывает соответствие специальности
        """
        if not resume_specialty:
            return 0.5
        
        # Ключевые слова для разных специальностей
        specialty_keywords = {
            'программист': ['разработчик', 'программист', 'developer', 'код', 'программирование'],
            'дизайнер': ['дизайн', 'дизайнер', 'ui', 'ux', 'графика', 'креатив'],
            'менеджер': ['менеджер', 'управление', 'проект', 'команда', 'лидерство'],
            'аналитик': ['анализ', 'аналитик', 'данные', 'исследование', 'статистика'],
            'маркетинг': ['маркетинг', 'реклама', 'продвижение', 'smm', 'контент']
        }
        
        resume_specialty_lower = resume_specialty.lower()
        vacancy_text = f"{vacancy_title} {vacancy_description}".lower()
        
        # Ищем ключевые слова специальности в тексте вакансии
        for specialty, keywords in specialty_keywords.items():
            if specialty in resume_specialty_lower:
                matches = sum(1 for keyword in keywords if keyword in vacancy_text)
                return min(1.0, matches / len(keywords))
        
        return 0.3  # Базовое соответствие
    
    def calculate_freshness_score(self, vacancy_created_at: datetime) -> float:
        """
        Рассчитывает оценку актуальности вакансии
        """
        days_old = (datetime.utcnow() - vacancy_created_at).days
        
        if days_old <= 7:
            return 1.0
        elif days_old <= 30:
            return 0.8
        elif days_old <= 90:
            return 0.6
        else:
            return 0.3
    
    def generate_recommendation_reason(self, resume: Resume, vacancy: Vacancy, 
                                    skill_score: float, experience_score: float,
                                    text_score: float, specialty_score: float) -> str:
        """
        Генерирует объяснение рекомендации
        """
        reasons = []
        
        if skill_score > 0.7:
            reasons.append("Высокое соответствие навыков")
        elif skill_score > 0.4:
            reasons.append("Частичное соответствие навыков")
        
        if experience_score > 0.8:
            reasons.append("Подходящий опыт работы")
        
        if text_score > 0.6:
            reasons.append("Схожие требования и опыт")
        
        if specialty_score > 0.7:
            reasons.append("Соответствие специальности")
        
        if not reasons:
            reasons.append("Общие требования подходят")
        
        return "; ".join(reasons)
    
    def get_recommendations_for_resume(self, resume_id: int, limit: int = 10) -> List[Dict]:
        """
        Получает рекомендации для конкретного резюме
        """
        resume = self.db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            return []
        
        # Получаем навыки резюме
        resume_skills = [skill.id for skill in resume.skills]
        
        # Получаем все активные вакансии
        active_vacancies = self.db.query(Vacancy).filter(
            Vacancy.status == "published"
        ).all()
        
        recommendations = []
        
        for vacancy in active_vacancies:
            # Проверяем, не откликался ли уже кандидат на эту вакансию
            existing_application = self.db.query(Application).filter(
                Application.vacancy_id == vacancy.id,
                Application.resume_id == resume_id
            ).first()
            
            if existing_application:
                continue
            
            # Получаем навыки вакансии
            vacancy_skills = [skill.id for skill in vacancy.skills]
            required_skills = [
                vs.skill_id for vs in vacancy.skills 
                if hasattr(vs, 'is_required') and vs.is_required
            ]
            
            # Рассчитываем различные оценки
            skill_score = self.calculate_skill_match_score(resume_skills, vacancy_skills, required_skills)
            experience_score = self.calculate_experience_score(0, vacancy.requirements or "")  # Предполагаем 0 лет опыта
            text_score = self.calculate_text_similarity(
                resume.summary or "", 
                f"{vacancy.title} {vacancy.description or ''}"
            )
            specialty_score = self.calculate_specialty_match(
                resume.specialty or "", 
                vacancy.title, 
                vacancy.description or ""
            )
            freshness_score = self.calculate_freshness_score(vacancy.created_at)
            
            # Итоговая оценка (взвешенная сумма)
            final_score = (
                skill_score * 0.4 +
                experience_score * 0.2 +
                text_score * 0.2 +
                specialty_score * 0.1 +
                freshness_score * 0.1
            )
            
            if final_score > 0.3:  # Минимальный порог для рекомендации
                reason = self.generate_recommendation_reason(
                    resume, vacancy, skill_score, experience_score, text_score, specialty_score
                )
                
                recommendations.append({
                    'vacancy_id': vacancy.id,
                    'vacancy_title': vacancy.title,
                    'company_name': vacancy.company.name if vacancy.company else "Неизвестная компания",
                    'score': final_score,
                    'reason': reason,
                    'skill_score': skill_score,
                    'experience_score': experience_score,
                    'text_score': text_score,
                    'specialty_score': specialty_score,
                    'freshness_score': freshness_score
                })
        
        # Сортируем по убыванию оценки
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        # Сохраняем рекомендации в БД
        for rec in recommendations[:limit]:
            existing_rec = self.db.query(Recommendation).filter(
                Recommendation.resume_id == resume_id,
                Recommendation.vacancy_id == rec['vacancy_id']
            ).first()
            
            if not existing_rec:
                new_rec = Recommendation(
                    resume_id=resume_id,
                    vacancy_id=rec['vacancy_id'],
                    score=rec['score'],
                    reason=rec['reason']
                )
                self.db.add(new_rec)
        
        self.db.commit()
        
        return recommendations[:limit]
    
    def get_recommendations_for_user(self, user_id: int, limit: int = 10) -> List[Dict]:
        """
        Получает рекомендации для пользователя (все его резюме)
        """
        user_resumes = self.db.query(Resume).filter(Resume.user_id == user_id).all()
        
        all_recommendations = []
        
        for resume in user_resumes:
            resume_recommendations = self.get_recommendations_for_resume(resume.id, limit)
            all_recommendations.extend(resume_recommendations)
        
        # Убираем дубликаты и сортируем
        unique_recommendations = {}
        for rec in all_recommendations:
            key = rec['vacancy_id']
            if key not in unique_recommendations or rec['score'] > unique_recommendations[key]['score']:
                unique_recommendations[key] = rec
        
        sorted_recommendations = sorted(
            unique_recommendations.values(), 
            key=lambda x: x['score'], 
            reverse=True
        )
        
        return sorted_recommendations[:limit]
