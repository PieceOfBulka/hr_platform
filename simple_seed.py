#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import create_tables, get_db, User, Company, Vacancy, ListOfSkills, Resume
from datetime import datetime, timedelta

def create_simple_data():
    """Создает простые тестовые данные"""
    try:
        print("Создаем таблицы...")
        create_tables()
        
        print("Подключаемся к БД...")
        db = next(get_db())
        
        # Создаем пользователя HR
        hr_user = User(
            email="hr@company.com",
            password_hash="hashed_password",
            role="hr",
            name_of_place="HR Manager"
        )
        db.add(hr_user)
        db.flush()
        
        # Создаем компанию
        company = Company(
            name="Test Company",
            description="Тестовая компания",
            contact_person="Иван Иванов",
            contact_email="ivan@company.com",
            contact_phone="+7-999-123-45-67",
            user_id=hr_user.id
        )
        db.add(company)
        db.flush()
        
        # Создаем навыки
        skills_data = [
            {"name": "Python", "category": "technical"},
            {"name": "JavaScript", "category": "technical"},
            {"name": "React", "category": "technical"},
            {"name": "SQL", "category": "technical"},
            {"name": "Коммуникабельность", "category": "soft"}
        ]
        
        skills = []
        for skill_data in skills_data:
            skill = ListOfSkills(**skill_data)
            db.add(skill)
            skills.append(skill)
        
        db.commit()
        print(f"✅ Создано {len(skills)} навыков")
        
        # Создаем вакансию
        vacancy = Vacancy(
            title="Python Developer",
            description="Разработка на Python",
            requirements="Знание Python, SQL",
            company_id=company.id,
            status="published",
            created_at=datetime.utcnow()
        )
        db.add(vacancy)
        db.flush()
        
        # Добавляем навыки к вакансии
        vacancy.skills = skills[:3]  # Python, JavaScript, React
        
        # Создаем соискателя
        applicant = User(
            email="applicant@email.com",
            password_hash="hashed_password",
            role="applicant",
            name_of_place="Соискатель"
        )
        db.add(applicant)
        db.flush()
        
        # Создаем резюме
        resume = Resume(
            full_name="Александр Иванов",
            email="alex@email.com",
            phone="+7-999-111-11-11",
            summary="Python разработчик",
            specialty="Python Developer",
            user_id=applicant.id
        )
        db.add(resume)
        db.flush()
        
        # Добавляем навыки к резюме
        resume.skills = skills[:2]  # Python, JavaScript
        
        db.commit()
        
        print("Test data created successfully!")
        print(f"   - HR User: {hr_user.id}")
        print(f"   - Company: {company.id}")
        print(f"   - Vacancy: {vacancy.id}")
        print(f"   - Applicant: {applicant.id}")
        print(f"   - Resume: {resume.id}")
        
        db.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_simple_data()
