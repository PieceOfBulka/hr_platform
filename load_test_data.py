#!/usr/bin/env python
"""
Скрипт для загрузки тестовых данных в SQLite
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import User
from vacancies.models import Vacancy, Application
from resumes.models import Resume, WorkExperience, Education
from recommendations.models import RecommendationRule

User = get_user_model()

def create_test_data():
    """Создает тестовые данные для системы рекомендаций"""
    
    print("🚀 Создание тестовых данных...")
    
    # 1. Создаем пользователей
    print("👥 Создание пользователей...")
    
    # Администратор
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Администратор',
            'last_name': 'Системы',
            'role': User.Role.ADMIN,
            'is_staff': True,
            'is_superuser': True,
            'is_verified': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✓ Администратор создан")
    
    # HR пользователи
    hr_users = [
        {
            'username': 'hr_tech',
            'email': 'hr@techcorp.ru',
            'first_name': 'Анна',
            'last_name': 'Петрова',
            'company': 'ТехКорп',
            'position': 'HR-менеджер'
        },
        {
            'username': 'hr_med',
            'email': 'hr@medcorp.ru',
            'first_name': 'Мария',
            'last_name': 'Сидорова',
            'company': 'МедКорп',
            'position': 'HR-директор'
        }
    ]
    
    for hr_data in hr_users:
        hr_user, created = User.objects.get_or_create(
            username=hr_data['username'],
            defaults={
                **hr_data,
                'role': User.Role.HR,
                'is_verified': True
            }
        )
        if created:
            hr_user.set_password('hr123')
            hr_user.save()
            print(f"✓ HR пользователь {hr_data['first_name']} создан")
    
    # Кандидаты
    candidates_data = [
        {
            'username': 'candidate1',
            'email': 'ivan@example.com',
            'first_name': 'Иван',
            'last_name': 'Петров',
            'phone': '+7 (901) 123-45-67'
        },
        {
            'username': 'candidate2',
            'email': 'maria@example.com',
            'first_name': 'Мария',
            'last_name': 'Соколова',
            'phone': '+7 (902) 234-56-78'
        },
        {
            'username': 'candidate3',
            'email': 'alex@example.com',
            'first_name': 'Алексей',
            'last_name': 'Смирнов',
            'phone': '+7 (903) 345-67-89'
        }
    ]
    
    for candidate_data in candidates_data:
        candidate, created = User.objects.get_or_create(
            username=candidate_data['username'],
            defaults={
                **candidate_data,
                'role': User.Role.CANDIDATE
            }
        )
        if created:
            candidate.set_password('candidate123')
            candidate.save()
            print(f"✓ Кандидат {candidate_data['first_name']} создан")
    
    # 2. Создаем резюме
    print("📄 Создание резюме...")
    
    resume_data = [
        {
            'user': User.objects.get(username='candidate1'),
            'title': 'Python разработчик',
            'summary': 'Опытный Python разработчик с 3 годами опыта. Знаю Django, Flask, PostgreSQL. Участвовал в разработке веб-приложений и API.',
            'skills': 'Python, Django, Flask, PostgreSQL, Git, Docker, Linux',
            'experience_level': Resume.ExperienceLevel.MIDDLE,
            'education_level': Resume.EducationLevel.BACHELOR,
            'university': 'МГУ',
            'faculty': 'Факультет ВМК',
            'graduation_year': 2020,
            'salary_expectation': 120000,
            'is_remote': True
        },
        {
            'user': User.objects.get(username='candidate2'),
            'title': 'Frontend разработчик',
            'summary': 'Специализируюсь на React и Vue.js. Опыт работы с современными фреймворками, TypeScript, Webpack.',
            'skills': 'JavaScript, React, Vue.js, TypeScript, HTML, CSS, Webpack',
            'experience_level': Resume.ExperienceLevel.JUNIOR,
            'education_level': Resume.EducationLevel.BACHELOR,
            'university': 'ВШЭ',
            'faculty': 'Факультет компьютерных наук',
            'graduation_year': 2022,
            'salary_expectation': 80000,
            'is_remote': False
        },
        {
            'user': User.objects.get(username='candidate3'),
            'title': 'Data Scientist',
            'summary': 'Специалист по машинному обучению и анализу данных. Опыт работы с Python, pandas, scikit-learn, TensorFlow.',
            'skills': 'Python, pandas, scikit-learn, TensorFlow, SQL, статистика, машинное обучение',
            'experience_level': Resume.ExperienceLevel.SENIOR,
            'education_level': Resume.EducationLevel.MASTER,
            'university': 'МФТИ',
            'faculty': 'Факультет управления и прикладной математики',
            'graduation_year': 2019,
            'salary_expectation': 150000,
            'is_remote': True
        }
    ]
    
    for resume_info in resume_data:
        resume, created = Resume.objects.get_or_create(
            user=resume_info['user'],
            defaults=resume_info
        )
        if created:
            print(f"✓ Резюме для {resume_info['user'].first_name} создано")
    
    # 3. Создаем вакансии
    print("💼 Создание вакансий...")
    
    hr_tech = User.objects.get(username='hr_tech')
    hr_med = User.objects.get(username='hr_med')
    
    vacancies_data = [
        {
            'title': 'Senior Python Developer',
            'description': 'Ищем опытного Python разработчика для работы над высоконагруженными системами. Требуется опыт работы с Django, PostgreSQL, Redis.',
            'requirements': 'Python, Django, PostgreSQL, Redis, Docker, опыт работы с микросервисами',
            'responsibilities': 'Разработка backend API, оптимизация производительности, работа в команде',
            'salary_min': 150000,
            'salary_max': 250000,
            'experience_level': Vacancy.ExperienceLevel.SENIOR,
            'company': hr_tech,
            'contact_email': 'hr@techcorp.ru',
            'is_remote': True,
            'status': Vacancy.Status.PUBLISHED
        },
        {
            'title': 'Frontend Developer (React)',
            'description': 'Разработка пользовательских интерфейсов для веб-приложений. Работа с современными технологиями и инструментами.',
            'requirements': 'JavaScript, React, TypeScript, HTML5, CSS3, опыт работы с REST API',
            'responsibilities': 'Создание компонентов React, интеграция с backend API, оптимизация производительности',
            'salary_min': 100000,
            'salary_max': 180000,
            'experience_level': Vacancy.ExperienceLevel.MIDDLE,
            'company': hr_tech,
            'contact_email': 'hr@techcorp.ru',
            'is_remote': False,
            'status': Vacancy.Status.PUBLISHED
        },
        {
            'title': 'Data Scientist',
            'description': 'Анализ больших данных, построение ML моделей, работа с алгоритмами машинного обучения.',
            'requirements': 'Python, pandas, scikit-learn, TensorFlow, SQL, статистика, опыт работы с большими данными',
            'responsibilities': 'Анализ данных, построение ML моделей, создание отчетов, работа с командой аналитиков',
            'salary_min': 120000,
            'salary_max': 200000,
            'experience_level': Vacancy.ExperienceLevel.SENIOR,
            'company': hr_med,
            'contact_email': 'hr@medcorp.ru',
            'is_remote': True,
            'status': Vacancy.Status.PUBLISHED
        },
        {
            'title': 'Junior Python Developer',
            'description': 'Стажировка для начинающих Python разработчиков. Обучение современным технологиям и практический опыт.',
            'requirements': 'Базовые знания Python, желание изучать Django, PostgreSQL, Git',
            'responsibilities': 'Изучение технологий, работа над небольшими задачами, участие в code review',
            'salary_min': 50000,
            'salary_max': 80000,
            'experience_level': Vacancy.ExperienceLevel.JUNIOR,
            'company': hr_tech,
            'contact_email': 'hr@techcorp.ru',
            'is_remote': False,
            'status': Vacancy.Status.PUBLISHED
        }
    ]
    
    for vacancy_info in vacancies_data:
        vacancy, created = Vacancy.objects.get_or_create(
            title=vacancy_info['title'],
            company=vacancy_info['company'],
            defaults=vacancy_info
        )
        if created:
            print(f"✓ Вакансия '{vacancy_info['title']}' создана")
    
    # 4. Создаем правила рекомендаций
    print("📋 Создание правил рекомендаций...")
    
    rules_data = [
        {
            'name': 'Совпадение навыков Python',
            'description': 'Проверка наличия навыков Python в резюме',
            'skill_keywords': 'python, django, flask',
            'weight': 2.0
        },
        {
            'name': 'Совпадение навыков Frontend',
            'description': 'Проверка навыков frontend разработки',
            'skill_keywords': 'javascript, react, vue, typescript',
            'weight': 2.0
        },
        {
            'name': 'Совпадение навыков Data Science',
            'description': 'Проверка навыков анализа данных',
            'skill_keywords': 'pandas, scikit-learn, tensorflow, машинное обучение',
            'weight': 2.0
        },
        {
            'name': 'Соответствие уровня опыта',
            'description': 'Проверка соответствия уровня опыта',
            'weight': 1.5
        },
        {
            'name': 'Соответствие зарплатных ожиданий',
            'description': 'Проверка соответствия зарплатных ожиданий',
            'weight': 1.0
        }
    ]
    
    for rule_info in rules_data:
        rule, created = RecommendationRule.objects.get_or_create(
            name=rule_info['name'],
            defaults=rule_info
        )
        if created:
            print(f"✓ Правило '{rule_info['name']}' создано")
    
    print("✅ Тестовые данные успешно созданы!")
    print("\n📋 Данные для входа:")
    print("👤 Администратор: admin / admin123")
    print("👤 HR (ТехКорп): hr_tech / hr123")
    print("👤 HR (МедКорп): hr_med / hr123")
    print("👤 Кандидат 1: candidate1 / candidate123")
    print("👤 Кандидат 2: candidate2 / candidate123")
    print("👤 Кандидат 3: candidate3 / candidate123")

if __name__ == '__main__':
    create_test_data()
