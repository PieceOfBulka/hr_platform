#!/usr/bin/env python3
"""
Скрипт для настройки AI системы рекомендаций
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Настройка переменных окружения"""
    print("🔧 Настройка AI системы рекомендаций...")
    
    # Проверяем наличие .env файла
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Создание .env файла...")
        with open(".env", "w", encoding="utf-8") as f:
            f.write("""# Конфигурация для HR Platform

# База данных
DATABASE_URL=sqlite:///./hr_platform.db

# Hugging Face API Token (получите на https://huggingface.co/settings/tokens)
# HUGGINGFACE_TOKEN=your_token_here

# Настройки сервера
HOST=127.0.0.1
PORT=8000

# Настройки логирования
LOG_LEVEL=INFO
""")
        print("✅ .env файл создан")
    else:
        print("✅ .env файл уже существует")
    
    # Проверяем токен Hugging Face
    huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
    if not huggingface_token:
        print("\n⚠️  Внимание: HUGGINGFACE_TOKEN не установлен!")
        print("Для получения токена:")
        print("1. Зайдите на https://huggingface.co/settings/tokens")
        print("2. Создайте новый токен")
        print("3. Добавьте его в .env файл: HUGGINGFACE_TOKEN=your_token_here")
        print("\n💡 Система будет работать без токена, но с ограниченной функциональностью")
    else:
        print("✅ Hugging Face токен найден")

def test_ai_system():
    """Тестирование AI системы"""
    print("\n🧪 Тестирование AI системы...")
    
    try:
        from ai_recommendation_engine import HuggingFaceAPI
        
        # Тестируем API
        hf_api = HuggingFaceAPI()
        test_texts = ["Python разработчик", "Java программист"]
        
        print("📡 Тестирование Hugging Face API...")
        embeddings = hf_api.get_embeddings(test_texts)
        
        if embeddings and len(embeddings) >= 2:
            similarity = hf_api.calculate_similarity(embeddings[0], embeddings[1])
            print(f"✅ API работает! Сходство тестовых текстов: {similarity:.3f}")
        else:
            print("⚠️  API не отвечает, используется fallback режим")
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

def create_sample_data():
    """Создание тестовых данных"""
    print("\n📊 Создание тестовых данных...")
    
    try:
        from database import create_tables, get_db, User, Resume, Vacancy, Company, ListOfSkills
        from sqlalchemy.orm import Session
        
        # Создаем таблицы
        create_tables()
        print("✅ Таблицы базы данных созданы")
        
        # Получаем сессию базы данных
        db = next(get_db())
        
        # Проверяем, есть ли уже данные
        user_count = db.query(User).count()
        if user_count > 0:
            print("✅ Данные уже существуют в базе")
            return
        
        # Создаем тестовые навыки
        skills_data = [
            ("Python", "technical"),
            ("Java", "technical"),
            ("JavaScript", "technical"),
            ("React", "technical"),
            ("SQL", "technical"),
            ("Git", "technical"),
            ("Коммуникабельность", "soft"),
            ("Лидерство", "soft"),
            ("Английский", "language"),
            ("Русский", "language"),
            ("Финансы", "domain"),
            ("Маркетинг", "domain")
        ]
        
        skills = []
        for name, category in skills_data:
            skill = ListOfSkills(name=name, category=category)
            db.add(skill)
            skills.append(skill)
        
        db.commit()
        print(f"✅ Создано {len(skills)} навыков")
        
        # Создаем тестовую компанию
        company = Company(
            name="ТехКорп",
            description="Инновационная IT компания",
            contact_person="Иван Петров",
            contact_email="hr@techcorp.ru"
        )
        db.add(company)
        db.commit()
        
        # Создаем тестовые вакансии
        vacancies_data = [
            {
                "title": "Python разработчик",
                "description": "Ищем опытного Python разработчика для работы с веб-приложениями",
                "requirements": "Опыт работы с Python, Django, PostgreSQL",
                "skills": ["Python", "SQL", "Git"]
            },
            {
                "title": "Frontend разработчик",
                "description": "Требуется разработчик для создания современных веб-интерфейсов",
                "requirements": "Знание JavaScript, React, HTML/CSS",
                "skills": ["JavaScript", "React", "Git"]
            },
            {
                "title": "Java разработчик",
                "description": "Ищем Java разработчика для корпоративных проектов",
                "requirements": "Опыт с Java, Spring Framework, базами данных",
                "skills": ["Java", "SQL", "Git"]
            }
        ]
        
        for vacancy_data in vacancies_data:
            vacancy = Vacancy(
                company_id=company.id,
                title=vacancy_data["title"],
                description=vacancy_data["description"],
                requirements=vacancy_data["requirements"],
                status="published"
            )
            db.add(vacancy)
            db.flush()
            
            # Добавляем навыки к вакансии
            vacancy_skills = [s for s in skills if s.name in vacancy_data["skills"]]
            vacancy.skills = vacancy_skills
        
        db.commit()
        print(f"✅ Создано {len(vacancies_data)} вакансий")
        
        # Создаем тестового пользователя и резюме
        user = User(
            email="test@example.com",
            password_hash="dummy_hash",
            role="applicant",
            name_of_place="Тестовый Пользователь"
        )
        db.add(user)
        db.flush()
        
        resume = Resume(
            full_name="Тестовый Пользователь",
            email="test@example.com",
            summary="Опытный разработчик с 3 годами опыта в Python и веб-разработке",
            specialty="Python разработчик",
            user_id=user.id
        )
        db.add(resume)
        db.flush()
        
        # Добавляем навыки к резюме
        resume_skills = [s for s in skills if s.name in ["Python", "SQL", "Git", "Коммуникабельность", "Английский"]]
        resume.skills = resume_skills
        
        db.commit()
        print("✅ Создано тестовое резюме (ID: 1)")
        
        print("\n🎯 Тестовые данные готовы!")
        print("Вы можете протестировать систему с ID резюме: 1")
        
    except Exception as e:
        print(f"❌ Ошибка при создании данных: {e}")

def main():
    """Основная функция"""
    print("🚀 Настройка AI системы рекомендаций для HR Platform")
    print("=" * 60)
    
    setup_environment()
    test_ai_system()
    create_sample_data()
    
    print("\n" + "=" * 60)
    print("✅ Настройка завершена!")
    print("\n📋 Следующие шаги:")
    print("1. Запустите сервер: python main.py")
    print("2. Откройте http://localhost:8000")
    print("3. Введите ID резюме: 1")
    print("4. Включите AI рекомендации и получите результаты!")
    
    if not os.getenv("HUGGINGFACE_TOKEN"):
        print("\n💡 Для полной функциональности добавьте HUGGINGFACE_TOKEN в .env файл")

if __name__ == "__main__":
    main()
