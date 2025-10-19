#!/usr/bin/env python
"""
Скрипт для импорта данных из готовой БД PostgreSQL
Использует данные из папки db_create_f
"""

import os
import sys
import django
import psycopg2
from django.core.management import execute_from_command_line

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_platform.settings')
django.setup()

def import_data_from_sql():
    """Импортирует данные из SQL файлов"""
    
    # Настройки подключения к БД
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'hr_platform',
        'user': 'postgres',
        'password': 'your-db-password'  # Замените на ваш пароль
    }
    
    try:
        # Подключение к БД
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Список SQL файлов для импорта
        sql_files = [
            'hr_platform/db_create_f/users_202510190226.sql',
            'hr_platform/db_create_f/companies_202510190226.sql',
            'hr_platform/db_create_f/vacancies_202510190226.sql',
            'hr_platform/db_create_f/resumes_202510190226.sql',
            'hr_platform/db_create_f/skills_202510190226.sql',
            'hr_platform/db_create_f/applications_202510190226.sql',
        ]
        
        for sql_file in sql_files:
            if os.path.exists(sql_file):
                print(f"Импортируем {sql_file}...")
                with open(sql_file, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                    
                # Выполняем SQL
                cursor.execute(sql_content)
                conn.commit()
                print(f"✓ {sql_file} импортирован успешно")
            else:
                print(f"⚠ Файл {sql_file} не найден")
        
        print("✅ Импорт данных завершен успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при импорте данных: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def setup_database():
    """Настройка базы данных"""
    print("Настройка базы данных...")
    
    # Создание миграций
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Применение миграций
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Создание суперпользователя (если нужно)
    print("Создание суперпользователя...")
    execute_from_command_line(['manage.py', 'createsuperuser', '--noinput', '--username', 'admin', '--email', 'admin@example.com'])
    
    print("✅ База данных настроена!")

if __name__ == '__main__':
    print("🚀 Начинаем настройку системы рекомендаций...")
    
    # 1. Настройка БД
    setup_database()
    
    # 2. Импорт данных
    import_data_from_sql()
    
    print("🎉 Система рекомендаций готова к работе!")
    print("\n📋 Следующие шаги:")
    print("1. Установите токен Hugging Face в файле env.local")
    print("2. Настройте подключение к PostgreSQL")
    print("3. Запустите сервер: python manage.py runserver")
    print("4. Перейдите на /recommendations/candidate/ для просмотра рекомендаций")
