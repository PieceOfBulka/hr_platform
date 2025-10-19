#!/usr/bin/env python3
"""
Тест локальной модели Gemma для системы рекомендаций
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_platform.settings')
django.setup()

from recommendations.services import GemmaRecommendationService

def test_local_model():
    """Тестирует локальную модель Gemma"""
    print("🤖 Тестирование локальной модели Gemma...")
    
    try:
        # Создаем сервис
        service = GemmaRecommendationService()
        
        if not service.model:
            print("❌ Модель не загружена!")
            return False
        
        print(f"✅ Модель загружена на устройство: {service.device}")
        
        # Тестовый промпт
        test_prompt = """
        Проанализируй соответствие кандидата и вакансии:
        
        КАНДИДАТ:
        - Навыки: Python, Django, PostgreSQL
        - Опыт: 3 года
        - Образование: Высшее
        
        ВАКАНСИЯ:
        - Требования: Python, Django, PostgreSQL
        - Опыт: 2+ года
        - Образование: Высшее
        
        Оцени от 0 до 10 и объясни почему.
        """
        
        print("📝 Отправляем тестовый запрос...")
        response = service._call_local_model(test_prompt)
        
        if response:
            print("✅ Получен ответ от модели:")
            print("-" * 50)
            print(response)
            print("-" * 50)
            return True
        else:
            print("❌ Не удалось получить ответ от модели")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = test_local_model()
    if success:
        print("\n🎉 Тест прошел успешно!")
    else:
        print("\n💥 Тест не прошел!")
        sys.exit(1)
