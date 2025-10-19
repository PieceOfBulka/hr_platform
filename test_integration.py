#!/usr/bin/env python3
"""
Тест интеграции локальной модели Gemma с Django сайтом
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from recommendations.services import RecommendationService

User = get_user_model()

def test_integration():
    """Тестирует интеграцию с сайтом"""
    print("🧪 Тестирование интеграции локальной модели с сайтом...")
    
    try:
        # Получаем тестового пользователя
        try:
            user = User.objects.filter(is_candidate=True).first()
            if not user:
                print("❌ Нет тестовых кандидатов в базе данных!")
                return False
            print(f"✅ Найден тестовый пользователь: {user.username}")
        except Exception as e:
            print(f"❌ Ошибка получения пользователя: {e}")
            return False
        
        # Тестируем сервис рекомендаций
        try:
            service = RecommendationService()
            print(f"✅ Сервис рекомендаций создан")
            
            # Проверяем модель
            if hasattr(service, 'gemma_service') and service.gemma_service.model:
                print(f"✅ Локальная модель Gemma загружена на {service.gemma_service.device}")
            else:
                print("⚠️ Локальная модель не загружена, будет использован fallback")
            
            # Получаем рекомендации
            recommendations = service.get_vacancy_recommendations_for_candidate(user)
            print(f"✅ Получено {len(recommendations)} рекомендаций")
            
            # Показываем первые 3 рекомендации
            for i, rec in enumerate(recommendations[:3]):
                print(f"  {i+1}. {rec['vacancy'].title} - {rec['score']:.1f}%")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сервиса рекомендаций: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        return False

if __name__ == "__main__":
    success = test_integration()
    if success:
        print("\n🎉 Интеграция работает успешно!")
        print("🌐 Откройте http://127.0.0.1:8000/recommendations/candidate/ для тестирования")
    else:
        print("\n💥 Интеграция не работает!")
        sys.exit(1)
