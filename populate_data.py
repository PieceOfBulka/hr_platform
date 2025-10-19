#!/usr/bin/env python
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_platform.settings')
django.setup()

# Импортируем и запускаем команду
from django.core.management import call_command

if __name__ == '__main__':
    try:
        print("Запуск команды заполнения базы данных...")
        call_command('populate_data', '--clear')
        print("Команда выполнена успешно!")
    except Exception as e:
        print(f"Ошибка при выполнении команды: {e}")
        sys.exit(1)
