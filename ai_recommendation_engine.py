import requests
import json
import numpy as np
from typing import List, Dict, Tuple, Optional
from sqlalchemy.orm import Session
from database import Resume, Vacancy, ListOfSkills, Company, Recommendation
from datetime import datetime
import logging
from dataclasses import dataclass
import re

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RecommendationResult:
    vacancy_id: int
    vacancy_title: str
    company_name: str
    score: float
    reason: str
    skill_score: float
    experience_score: float
    text_score: float
    specialty_score: float
    freshness_score: float

class HuggingFaceAPI:
    """Класс для работы с Hugging Face API"""
    
    def __init__(self, api_token: str = None):
        self.api_token = api_token
        self.base_url = "https://api-inference.huggingface.co/models"
        self.headers = {
            "Authorization": f"Bearer {api_token}" if api_token else None,
            "Content-Type": "application/json"
        }
    
    def get_embeddings(self, texts: List[str], model: str = "sentence-transformers/all-MiniLM-L6-v2") -> List[List[float]]:
        """Получить эмбеддинги для текстов"""
        try:
            url = f"{self.base_url}/{model}"
            
            # Если нет токена, используем публичный API (с ограничениями)
            if not self.api_token:
                url = f"https://api-inference.huggingface.co/models/{model}"
                headers = {"Content-Type": "application/json"}
            else:
                headers = self.headers
            
            payload = {
                "inputs": texts,
                "options": {"wait_for_model": True}
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"HuggingFace API error: {response.status_code} - {response.text}")
                return self._fallback_embeddings(texts)
                
        except Exception as e:
            logger.error(f"Error getting embeddings: {e}")
            return self._fallback_embeddings(texts)
    
    def _fallback_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Fallback метод для создания простых эмбеддингов"""
        embeddings = []
        for text in texts:
            # Простое создание эмбеддинга на основе длины и слов
            words = text.lower().split()
            embedding = [0.0] * 384  # Размер эмбеддинга для all-MiniLM-L6-v2
            
            # Заполняем эмбеддинг на основе характеристик текста
            embedding[0] = len(text) / 1000.0  # Нормализованная длина
            embedding[1] = len(words) / 100.0  # Количество слов
            embedding[2] = len(set(words)) / len(words) if words else 0  # Уникальность слов
            
            # Добавляем веса для ключевых слов
            tech_keywords = ['python', 'java', 'javascript', 'react', 'angular', 'vue', 'node', 'sql', 'database', 'api', 'web', 'mobile', 'frontend', 'backend', 'fullstack']
            for i, keyword in enumerate(tech_keywords[:10]):
                if keyword in text.lower():
                    embedding[3 + i] = 1.0
            
            embeddings.append(embedding)
        
        return embeddings
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Вычислить косинусное сходство между эмбеддингами"""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return max(0.0, min(1.0, similarity))  # Ограничиваем от 0 до 1
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0

class AIRecommendationEngine:
    """Улучшенная система рекомендаций с использованием AI"""
    
    def __init__(self, db: Session, huggingface_token: str = None):
        self.db = db
        self.hf_api = HuggingFaceAPI(huggingface_token)
        self.skill_weights = {
            'technical': 0.4,
            'soft': 0.2,
            'language': 0.15,
            'domain': 0.25
        }
    
    def get_recommendations_for_resume(self, resume_id: int, limit: int = 10) -> List[RecommendationResult]:
        """Получить рекомендации для конкретного резюме"""
        try:
            # Получаем резюме
            resume = self.db.query(Resume).filter(Resume.id == resume_id).first()
            if not resume:
                raise ValueError(f"Resume with id {resume_id} not found")
            
            # Получаем активные вакансии
            vacancies = self.db.query(Vacancy).filter(
                Vacancy.status == "published"
            ).all()
            
            if not vacancies:
                return []
            
            # Получаем рекомендации
            recommendations = []
            for vacancy in vacancies:
                score, reason, scores = self._calculate_compatibility(resume, vacancy)
                
                if score > 0.1:  # Минимальный порог совместимости
                    recommendations.append(RecommendationResult(
                        vacancy_id=vacancy.id,
                        vacancy_title=vacancy.title,
                        company_name=vacancy.company.name if vacancy.company else "Неизвестная компания",
                        score=score,
                        reason=reason,
                        skill_score=scores['skill_score'],
                        experience_score=scores['experience_score'],
                        text_score=scores['text_score'],
                        specialty_score=scores['specialty_score'],
                        freshness_score=scores['freshness_score']
                    ))
            
            # Сортируем по убыванию оценки
            recommendations.sort(key=lambda x: x.score, reverse=True)
            
            # Сохраняем рекомендации в базу данных
            self._save_recommendations(resume_id, recommendations[:limit])
            
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            return []
    
    def get_recommendations_for_user(self, user_id: int, limit: int = 10) -> List[RecommendationResult]:
        """Получить рекомендации для пользователя (по всем его резюме)"""
        try:
            # Получаем все резюме пользователя
            resumes = self.db.query(Resume).filter(Resume.user_id == user_id).all()
            
            if not resumes:
                return []
            
            # Получаем рекомендации для каждого резюме
            all_recommendations = []
            for resume in resumes:
                recommendations = self.get_recommendations_for_resume(resume.id, limit)
                all_recommendations.extend(recommendations)
            
            # Убираем дубликаты и сортируем
            unique_recommendations = {}
            for rec in all_recommendations:
                if rec.vacancy_id not in unique_recommendations or rec.score > unique_recommendations[rec.vacancy_id].score:
                    unique_recommendations[rec.vacancy_id] = rec
            
            result = list(unique_recommendations.values())
            result.sort(key=lambda x: x.score, reverse=True)
            
            return result[:limit]
            
        except Exception as e:
            logger.error(f"Error getting user recommendations: {e}")
            return []
    
    def _calculate_compatibility(self, resume: Resume, vacancy: Vacancy) -> Tuple[float, str, Dict[str, float]]:
        """Вычислить совместимость резюме и вакансии"""
        try:
            # 1. Анализ навыков (40% веса)
            skill_score = self._calculate_skill_compatibility(resume, vacancy)
            
            # 2. Анализ текста (30% веса)
            text_score = self._calculate_text_compatibility(resume, vacancy)
            
            # 3. Анализ специализации (20% веса)
            specialty_score = self._calculate_specialty_compatibility(resume, vacancy)
            
            # 4. Свежесть вакансии (10% веса)
            freshness_score = self._calculate_freshness_score(vacancy)
            
            # Итоговая оценка
            total_score = (
                skill_score * 0.4 +
                text_score * 0.3 +
                specialty_score * 0.2 +
                freshness_score * 0.1
            )
            
            # Генерируем объяснение
            reason = self._generate_reason(skill_score, text_score, specialty_score, freshness_score, resume, vacancy)
            
            scores = {
                'skill_score': skill_score,
                'experience_score': 0.0,  # Пока не реализовано
                'text_score': text_score,
                'specialty_score': specialty_score,
                'freshness_score': freshness_score
            }
            
            return total_score, reason, scores
            
        except Exception as e:
            logger.error(f"Error calculating compatibility: {e}")
            return 0.0, "Ошибка при расчете совместимости", {}
    
    def _calculate_skill_compatibility(self, resume: Resume, vacancy: Vacancy) -> float:
        """Вычислить совместимость навыков"""
        try:
            resume_skills = set(skill.id for skill in resume.skills)
            vacancy_skills = set(skill.id for skill in vacancy.skills)
            
            if not vacancy_skills:
                return 0.5  # Если у вакансии нет навыков, даем среднюю оценку
            
            # Количество совпадающих навыков
            common_skills = resume_skills.intersection(vacancy_skills)
            skill_match_ratio = len(common_skills) / len(vacancy_skills)
            
            # Учитываем категории навыков
            category_scores = {}
            for skill in resume.skills:
                if skill.id in common_skills:
                    category = skill.category or 'technical'
                    category_scores[category] = category_scores.get(category, 0) + 1
            
            # Взвешенная оценка по категориям
            weighted_score = 0
            total_weight = 0
            for category, count in category_scores.items():
                weight = self.skill_weights.get(category, 0.2)
                weighted_score += count * weight
                total_weight += weight
            
            if total_weight > 0:
                category_bonus = weighted_score / total_weight * 0.2
            else:
                category_bonus = 0
            
            final_score = min(1.0, skill_match_ratio + category_bonus)
            return final_score
            
        except Exception as e:
            logger.error(f"Error calculating skill compatibility: {e}")
            return 0.0
    
    def _calculate_text_compatibility(self, resume: Resume, vacancy: Vacancy) -> float:
        """Вычислить совместимость на основе текстового анализа"""
        try:
            # Подготавливаем тексты для анализа
            resume_text = f"{resume.summary or ''} {resume.specialty or ''}"
            vacancy_text = f"{vacancy.description or ''} {vacancy.requirements or ''}"
            
            if not resume_text.strip() or not vacancy_text.strip():
                return 0.3  # Базовая оценка если нет текста
            
            # Получаем эмбеддинги
            embeddings = self.hf_api.get_embeddings([resume_text, vacancy_text])
            
            if len(embeddings) >= 2:
                similarity = self.hf_api.calculate_similarity(embeddings[0], embeddings[1])
                return similarity
            else:
                # Fallback: простое сравнение ключевых слов
                return self._simple_text_similarity(resume_text, vacancy_text)
                
        except Exception as e:
            logger.error(f"Error calculating text compatibility: {e}")
            return 0.0
    
    def _simple_text_similarity(self, text1: str, text2: str) -> float:
        """Простое сравнение текстов на основе ключевых слов"""
        try:
            # Извлекаем ключевые слова
            words1 = set(re.findall(r'\b\w+\b', text1.lower()))
            words2 = set(re.findall(r'\b\w+\b', text2.lower()))
            
            if not words1 or not words2:
                return 0.0
            
            # Убираем стоп-слова
            stop_words = {'и', 'в', 'на', 'с', 'по', 'для', 'от', 'до', 'из', 'к', 'о', 'у', 'за', 'при', 'через', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            words1 = words1 - stop_words
            words2 = words2 - stop_words
            
            if not words1 or not words2:
                return 0.0
            
            # Вычисляем пересечение
            common_words = words1.intersection(words2)
            similarity = len(common_words) / max(len(words1), len(words2))
            
            return min(1.0, similarity)
            
        except Exception as e:
            logger.error(f"Error in simple text similarity: {e}")
            return 0.0
    
    def _calculate_specialty_compatibility(self, resume: Resume, vacancy: Vacancy) -> float:
        """Вычислить совместимость специализаций"""
        try:
            if not resume.specialty or not vacancy.title:
                return 0.5
            
            # Простое сравнение специализаций
            resume_specialty = resume.specialty.lower()
            vacancy_title = vacancy.title.lower()
            
            # Ключевые слова для разных специализаций
            specialty_keywords = {
                'разработчик': ['developer', 'программист', 'разработчик', 'developer'],
                'аналитик': ['аналитик', 'analyst', 'анализ', 'analysis'],
                'дизайнер': ['дизайнер', 'designer', 'дизайн', 'design'],
                'менеджер': ['менеджер', 'manager', 'руководитель', 'lead'],
                'тестировщик': ['тестировщик', 'tester', 'qa', 'тестирование', 'testing']
            }
            
            # Ищем совпадения
            for specialty, keywords in specialty_keywords.items():
                if any(keyword in resume_specialty for keyword in keywords):
                    if any(keyword in vacancy_title for keyword in keywords):
                        return 0.9
                    else:
                        return 0.3
            
            return 0.5  # Базовая оценка
            
        except Exception as e:
            logger.error(f"Error calculating specialty compatibility: {e}")
            return 0.0
    
    def _calculate_freshness_score(self, vacancy: Vacancy) -> float:
        """Вычислить оценку свежести вакансии"""
        try:
            if not vacancy.created_at:
                return 0.5
            
            # Вычисляем возраст вакансии в днях
            days_old = (datetime.utcnow() - vacancy.created_at).days
            
            # Чем новее вакансия, тем выше оценка
            if days_old <= 7:
                return 1.0
            elif days_old <= 30:
                return 0.8
            elif days_old <= 90:
                return 0.6
            else:
                return 0.4
                
        except Exception as e:
            logger.error(f"Error calculating freshness score: {e}")
            return 0.5
    
    def _generate_reason(self, skill_score: float, text_score: float, specialty_score: float, 
                        freshness_score: float, resume: Resume, vacancy: Vacancy) -> str:
        """Генерировать объяснение рекомендации"""
        try:
            reasons = []
            
            if skill_score > 0.7:
                reasons.append("Отличное совпадение навыков")
            elif skill_score > 0.5:
                reasons.append("Хорошее совпадение навыков")
            elif skill_score > 0.3:
                reasons.append("Частичное совпадение навыков")
            
            if text_score > 0.7:
                reasons.append("Высокая совместимость по описанию")
            elif text_score > 0.5:
                reasons.append("Совместимость по описанию")
            
            if specialty_score > 0.7:
                reasons.append("Совпадение специализации")
            
            if freshness_score > 0.8:
                reasons.append("Свежая вакансия")
            
            if not reasons:
                reasons.append("Базовая совместимость")
            
            return "; ".join(reasons)
            
        except Exception as e:
            logger.error(f"Error generating reason: {e}")
            return "Рекомендация на основе анализа профиля"
    
    def _save_recommendations(self, resume_id: int, recommendations: List[RecommendationResult]):
        """Сохранить рекомендации в базу данных"""
        try:
            for rec in recommendations:
                # Проверяем, есть ли уже такая рекомендация
                existing = self.db.query(Recommendation).filter(
                    Recommendation.resume_id == resume_id,
                    Recommendation.vacancy_id == rec.vacancy_id
                ).first()
                
                if existing:
                    # Обновляем существующую
                    existing.score = rec.score
                    existing.reason = rec.reason
                    existing.created_at = datetime.utcnow()
                else:
                    # Создаем новую
                    new_rec = Recommendation(
                        resume_id=resume_id,
                        vacancy_id=rec.vacancy_id,
                        score=rec.score,
                        reason=rec.reason
                    )
                    self.db.add(new_rec)
            
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error saving recommendations: {e}")
            self.db.rollback()

# Функция для создания экземпляра движка
def create_ai_recommendation_engine(db: Session, huggingface_token: str = None) -> AIRecommendationEngine:
    """Создать экземпляр AI Recommendation Engine"""
    return AIRecommendationEngine(db, huggingface_token)