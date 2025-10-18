from sqlalchemy.orm import Session
from database import (
    get_db, create_tables, User, Company, Vacancy, ListOfSkills, 
    Resume, Application
)
from datetime import datetime, timedelta
import random

def create_test_data():
    """Создает тестовые данные для демонстрации системы рекомендаций"""
    
    # Создаем таблицы
    create_tables()
    
    # Получаем сессию БД
    db = next(get_db())
    
    try:
        # Создаем навыки
        skills_data = [
            # Технические навыки
            {"name": "Python", "category": "technical"},
            {"name": "JavaScript", "category": "technical"},
            {"name": "React", "category": "technical"},
            {"name": "Node.js", "category": "technical"},
            {"name": "SQL", "category": "technical"},
            {"name": "Git", "category": "technical"},
            {"name": "Docker", "category": "technical"},
            {"name": "AWS", "category": "technical"},
            {"name": "Machine Learning", "category": "technical"},
            {"name": "Data Analysis", "category": "technical"},
            
            # Soft skills
            {"name": "Коммуникабельность", "category": "soft"},
            {"name": "Лидерство", "category": "soft"},
            {"name": "Работа в команде", "category": "soft"},
            {"name": "Управление проектами", "category": "soft"},
            {"name": "Креативность", "category": "soft"},
            
            # Языки
            {"name": "Английский", "category": "language"},
            {"name": "Немецкий", "category": "language"},
            {"name": "Французский", "category": "language"},
        ]
        
        skills = []
        for skill_data in skills_data:
            skill = ListOfSkills(**skill_data)
            db.add(skill)
            skills.append(skill)
        
        db.commit()
        
        # Создаем пользователей HR
        hr_users = []
        for i in range(3):
            user = User(
                email=f"hr{i+1}@company.com",
                password_hash="hashed_password",
                role="hr",
                name_of_place=f"HR Manager {i+1}"
            )
            db.add(user)
            hr_users.append(user)
        
        db.commit()
        
        # Создаем компании
        companies_data = [
            {
                "name": "TechCorp",
                "description": "Ведущая IT-компания",
                "contact_person": "Иван Петров",
                "contact_email": "ivan@techcorp.com",
                "contact_phone": "+7-999-123-45-67"
            },
            {
                "name": "DataSoft",
                "description": "Компания по анализу данных",
                "contact_person": "Мария Сидорова",
                "contact_email": "maria@datasoft.com",
                "contact_phone": "+7-999-234-56-78"
            },
            {
                "name": "WebStudio",
                "description": "Веб-разработка и дизайн",
                "contact_person": "Алексей Козлов",
                "contact_email": "alex@webstudio.com",
                "contact_phone": "+7-999-345-67-89"
            }
        ]
        
        companies = []
        for i, company_data in enumerate(companies_data):
            company = Company(
                **company_data,
                user_id=hr_users[i].id
            )
            db.add(company)
            companies.append(company)
        
        db.commit()
        
        # Создаем вакансии
        vacancies_data = [
            {
                "title": "Python Developer",
                "description": "Разработка веб-приложений на Python. Опыт работы с Django, Flask. Знание SQL, Git.",
                "requirements": "Опыт работы от 2 лет. Знание Python, Django, SQL. Опыт работы с Git.",
                "company_id": companies[0].id,
                "status": "published",
                "created_at": datetime.utcnow() - timedelta(days=5)
            },
            {
                "title": "Frontend Developer",
                "description": "Разработка пользовательских интерфейсов. React, JavaScript, HTML/CSS.",
                "requirements": "Опыт работы от 1 года. Знание React, JavaScript, HTML, CSS.",
                "company_id": companies[0].id,
                "status": "published",
                "created_at": datetime.utcnow() - timedelta(days=3)
            },
            {
                "title": "Data Analyst",
                "description": "Анализ данных, создание отчетов. Python, SQL, статистика.",
                "requirements": "Опыт работы от 1 года. Знание Python, SQL, статистика. Английский язык.",
                "company_id": companies[1].id,
                "status": "published",
                "created_at": datetime.utcnow() - timedelta(days=7)
            },
            {
                "title": "UI/UX Designer",
                "description": "Дизайн пользовательских интерфейсов. Figma, Adobe Creative Suite.",
                "requirements": "Опыт работы от 2 лет. Знание Figma, Adobe Creative Suite. Портфолио.",
                "company_id": companies[2].id,
                "status": "published",
                "created_at": datetime.utcnow() - timedelta(days=2)
            },
            {
                "title": "Full Stack Developer",
                "description": "Полный цикл разработки. Python, JavaScript, React, Node.js, SQL.",
                "requirements": "Опыт работы от 3 лет. Знание Python, JavaScript, React, Node.js, SQL, Git.",
                "company_id": companies[0].id,
                "status": "published",
                "created_at": datetime.utcnow() - timedelta(days=1)
            }
        ]
        
        vacancies = []
        for vacancy_data in vacancies_data:
            vacancy = Vacancy(**vacancy_data)
            db.add(vacancy)
            vacancies.append(vacancy)
        
        db.commit()
        
        # Добавляем навыки к вакансиям
        vacancy_skills_mapping = [
            # Python Developer
            [0, 4, 5],  # Python, SQL, Git
            # Frontend Developer  
            [1, 2],     # JavaScript, React
            # Data Analyst
            [0, 4, 8, 9],  # Python, SQL, Machine Learning, Data Analysis
            # UI/UX Designer
            [14],       # Креативность
            # Full Stack Developer
            [0, 1, 2, 3, 4, 5],  # Python, JavaScript, React, Node.js, SQL, Git
        ]
        
        for i, vacancy in enumerate(vacancies):
            if i < len(vacancy_skills_mapping):
                skill_ids = vacancy_skills_mapping[i]
                vacancy_skills = [skills[skill_id] for skill_id in skill_ids]
                vacancy.skills = vacancy_skills
        
        db.commit()
        
        # Создаем пользователей-соискателей
        applicants = []
        for i in range(5):
            user = User(
                email=f"applicant{i+1}@email.com",
                password_hash="hashed_password",
                role="applicant",
                name_of_place=f"Соискатель {i+1}"
            )
            db.add(user)
            applicants.append(user)
        
        db.commit()
        
        # Создаем резюме
        resumes_data = [
            {
                "full_name": "Александр Иванов",
                "email": "alex@email.com",
                "phone": "+7-999-111-11-11",
                "summary": "Python разработчик с опытом работы 3 года. Знаю Django, Flask, SQL, Git. Работал с веб-приложениями.",
                "specialty": "Python Developer",
                "user_id": applicants[0].id,
                "skill_ids": [0, 4, 5, 6]  # Python, SQL, Git, Docker
            },
            {
                "full_name": "Елена Петрова",
                "email": "elena@email.com",
                "phone": "+7-999-222-22-22",
                "summary": "Frontend разработчик. React, JavaScript, HTML, CSS. Опыт работы 2 года.",
                "specialty": "Frontend Developer",
                "user_id": applicants[1].id,
                "skill_ids": [1, 2, 10]  # JavaScript, React, Коммуникабельность
            },
            {
                "full_name": "Михаил Сидоров",
                "email": "mikhail@email.com",
                "phone": "+7-999-333-33-33",
                "summary": "Аналитик данных. Python, SQL, статистика, машинное обучение. Опыт работы 4 года.",
                "specialty": "Data Analyst",
                "user_id": applicants[2].id,
                "skill_ids": [0, 4, 8, 9, 15]  # Python, SQL, ML, Data Analysis, English
            },
            {
                "full_name": "Анна Козлова",
                "email": "anna@email.com",
                "phone": "+7-999-444-44-44",
                "summary": "UI/UX дизайнер. Figma, Adobe Creative Suite. Креативный подход к решению задач.",
                "specialty": "UI/UX Designer",
                "user_id": applicants[3].id,
                "skill_ids": [14, 10, 15]  # Креативность, Коммуникабельность, English
            },
            {
                "full_name": "Дмитрий Волков",
                "email": "dmitry@email.com",
                "phone": "+7-999-555-55-55",
                "summary": "Full Stack разработчик. Python, JavaScript, React, Node.js, SQL, Git. Опыт работы 5 лет.",
                "specialty": "Full Stack Developer",
                "user_id": applicants[4].id,
                "skill_ids": [0, 1, 2, 3, 4, 5, 6, 7]  # Все технические навыки
            }
        ]
        
        resumes = []
        for resume_data in resumes_data:
            skill_ids = resume_data.pop('skill_ids')
            resume = Resume(**resume_data)
            db.add(resume)
            db.flush()  # Получаем ID резюме
            
            # Добавляем навыки
            resume_skills = [skills[skill_id] for skill_id in skill_ids]
            resume.skills = resume_skills
            resumes.append(resume)
        
        db.commit()
        
        print("✅ Тестовые данные успешно созданы!")
        print(f"📊 Создано:")
        print(f"   - {len(skills)} навыков")
        print(f"   - {len(companies)} компаний")
        print(f"   - {len(vacancies)} вакансий")
        print(f"   - {len(resumes)} резюме")
        print(f"   - {len(applicants)} соискателей")
        print("\n🎯 Для тестирования рекомендаций используйте ID резюме от 1 до 5")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при создании тестовых данных: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
