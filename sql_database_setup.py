#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import glob
from pathlib import Path

def setup_database_from_sql():
    """
    Создает базу данных из SQL файлов из ветки data_base_script
    """
    print("Setting up database from SQL files...")
    
    # Создаем подключение к SQLite
    db_path = "hr_platform_from_sql.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ищем SQL файлы
    sql_files = glob.glob("*.sql")
    
    if not sql_files:
        print("SQL files not found. Make sure files are copied from data_base_script branch")
        return None
    
    print(f"Found {len(sql_files)} SQL files:")
    for file in sql_files:
        print(f"   - {file}")
    
    # Выполняем SQL файлы в правильном порядке
    execution_order = [
        "users.sql",
        "companies.sql", 
        "list_of_skills.sql",
        "vacancies.sql",
        "resumes.sql",
        "applications.sql"
    ]
    
    executed_files = []
    
    for sql_file in execution_order:
        if sql_file in sql_files:
            try:
                print(f"Executing {sql_file}...")
                with open(sql_file, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                
                # Разделяем на отдельные запросы
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                
                for statement in statements:
                    if statement:
                        cursor.execute(statement)
                
                executed_files.append(sql_file)
                print(f"Successfully executed {sql_file}")
                
            except Exception as e:
                print(f"Error in {sql_file}: {e}")
                continue
    
    # Выполняем оставшиеся файлы
    remaining_files = [f for f in sql_files if f not in executed_files]
    for sql_file in remaining_files:
        try:
            print(f"Executing {sql_file}...")
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            for statement in statements:
                if statement:
                    cursor.execute(statement)
            
            executed_files.append(sql_file)
            print(f"Successfully executed {sql_file}")
            
        except Exception as e:
            print(f"Error in {sql_file}: {e}")
            continue
    
    conn.commit()
    
    # Проверяем созданные таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\nCreated tables: {len(tables)}")
    for table in tables:
        print(f"   - {table[0]}")
    
    # Проверяем данные
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        print(f"   {table_name}: {count} records")
    
    conn.close()
    
    print(f"\nDatabase created: {db_path}")
    return db_path

def create_sample_data():
    """
    Создает тестовые данные для демонстрации
    """
    print("\nCreating sample data...")
    
    conn = sqlite3.connect("hr_platform_from_sql.db")
    cursor = conn.cursor()
    
    # Добавляем тестовые навыки
    skills_data = [
        ("Python", "technical"),
        ("JavaScript", "technical"),
        ("React", "technical"),
        ("SQL", "technical"),
        ("Git", "technical"),
        ("Коммуникабельность", "soft"),
        ("Лидерство", "soft"),
        ("Английский", "language")
    ]
    
    for skill_name, category in skills_data:
        cursor.execute(
            "INSERT OR IGNORE INTO list_of_skills (name, category) VALUES (?, ?)",
            (skill_name, category)
        )
    
    # Добавляем тестового пользователя HR
    cursor.execute("""
        INSERT OR IGNORE INTO users (email, password_hash, role, name_of_place, is_verified)
        VALUES (?, ?, ?, ?, ?)
    """, ("hr@company.com", "hashed_password", "hr", "HR Manager", True))
    
    # Добавляем компанию
    cursor.execute("""
        INSERT OR IGNORE INTO companies (name, description, contact_person, contact_email, contact_phone, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("TechCorp", "IT компания", "Иван Петров", "ivan@techcorp.com", "+7-999-123-45-67", 1))
    
    # Добавляем тестовую вакансию
    cursor.execute("""
        INSERT OR IGNORE INTO vacancies (company_id, title, description, requirements, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (1, "Python Developer", "Разработка на Python", "Знание Python, SQL, Git", "published", "2024-01-15 10:00:00"))
    
    # Добавляем тестового соискателя
    cursor.execute("""
        INSERT OR IGNORE INTO users (email, password_hash, role, name_of_place, is_verified)
        VALUES (?, ?, ?, ?, ?)
    """, ("applicant@email.com", "hashed_password", "applicant", "Александр Иванов", True))
    
    # Добавляем резюме
    cursor.execute("""
        INSERT OR IGNORE INTO resumes (full_name, email, phone, summary, specialty, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("Александр Иванов", "alex@email.com", "+7-999-111-11-11", 
          "Python разработчик с опытом 3 года", "Python Developer", 2))
    
    # Связываем навыки с вакансией
    cursor.execute("SELECT id FROM list_of_skills WHERE name IN ('Python', 'SQL', 'Git')")
    skill_ids = [row[0] for row in cursor.fetchall()]
    
    for skill_id in skill_ids:
        cursor.execute("""
            INSERT OR IGNORE INTO vacancy_skills (vacancy_id, skill_id, is_required, priority)
            VALUES (?, ?, ?, ?)
        """, (1, skill_id, True, 1))
    
    # Связываем навыки с резюме
    cursor.execute("SELECT id FROM list_of_skills WHERE name IN ('Python', 'JavaScript')")
    skill_ids = [row[0] for row in cursor.fetchall()]
    
    for skill_id in skill_ids:
        cursor.execute("""
            INSERT OR IGNORE INTO resume_skills (resume_id, skill_id)
            VALUES (?, ?)
        """, (1, skill_id))
    
    conn.commit()
    conn.close()
    
    print("Sample data created")

if __name__ == "__main__":
    # Создаем базу данных из SQL файлов
    db_path = setup_database_from_sql()
    
    if db_path:
        # Создаем тестовые данные
        create_sample_data()
        
        print("\nSetup completed!")
        print("Database: hr_platform_from_sql.db")
        print("For AI usage, add Hugging Face token to .env file")
        print("Run: python ai_main.py")
