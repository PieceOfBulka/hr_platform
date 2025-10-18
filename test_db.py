#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database import create_tables, get_db
    print("Импорт database.py успешен")
    
    # Создаем таблицы
    create_tables()
    print("Таблицы созданы успешно")
    
    # Тестируем подключение к БД
    db = next(get_db())
    print("Подключение к БД успешно")
    
    db.close()
    print("Все тесты прошли успешно!")
    
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()
