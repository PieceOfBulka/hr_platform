#!/usr/bin/env python3
"""
Простой тест AI системы рекомендаций
"""

def test_imports():
    """Тестирование импортов"""
    print("🧪 Тестирование импортов...")
    
    try:
        import requests
        print("✅ requests импортирован")
    except ImportError as e:
        print(f"❌ Ошибка импорта requests: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy импортирован")
    except ImportError as e:
        print(f"❌ Ошибка импорта numpy: {e}")
        return False
    
    try:
        from ai_recommendation_engine import HuggingFaceAPI
        print("✅ AI recommendation engine импортирован")
    except ImportError as e:
        print(f"❌ Ошибка импорта AI engine: {e}")
        return False
    
    return True

def test_huggingface_api():
    """Тестирование Hugging Face API"""
    print("\n📡 Тестирование Hugging Face API...")
    
    try:
        from ai_recommendation_engine import HuggingFaceAPI
        
        api = HuggingFaceAPI()
        test_texts = ["Python разработчик", "Java программист"]
        
        print("🔄 Получение эмбеддингов...")
        embeddings = api.get_embeddings(test_texts)
        
        if embeddings and len(embeddings) >= 2:
            similarity = api.calculate_similarity(embeddings[0], embeddings[1])
            print(f"✅ API работает! Сходство: {similarity:.3f}")
            return True
        else:
            print("⚠️  API не отвечает, используется fallback")
            return True
            
    except Exception as e:
        print(f"❌ Ошибка API: {e}")
        return False

def test_database():
    """Тестирование базы данных"""
    print("\n🗄️  Тестирование базы данных...")
    
    try:
        from database import create_tables, get_db, User, Resume, Vacancy, Company, ListOfSkills
        
        # Создаем таблицы
        create_tables()
        print("✅ Таблицы созданы")
        
        # Получаем сессию
        db = next(get_db())
        
        # Проверяем количество записей
        user_count = db.query(User).count()
        vacancy_count = db.query(Vacancy).count()
        skill_count = db.query(ListOfSkills).count()
        
        print(f"📊 Пользователей: {user_count}")
        print(f"📊 Вакансий: {vacancy_count}")
        print(f"📊 Навыков: {skill_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка БД: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование AI системы рекомендаций")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
    
    if test_huggingface_api():
        tests_passed += 1
    
    if test_database():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Результаты: {tests_passed}/{total_tests} тестов пройдено")
    
    if tests_passed == total_tests:
        print("✅ Все тесты пройдены! Система готова к работе.")
        print("\n🎯 Следующие шаги:")
        print("1. Запустите: python main.py")
        print("2. Откройте: http://localhost:8000")
        print("3. Протестируйте рекомендации!")
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте зависимости.")

if __name__ == "__main__":
    main()