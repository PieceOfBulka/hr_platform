#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_api():
    """Тестирует API рекомендаций"""
    try:
        # Тестируем главную страницу
        print("🌐 Тестируем главную страницу...")
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Главная страница работает")
        else:
            print(f"❌ Ошибка главной страницы: {response.status_code}")
        
        # Тестируем API рекомендаций
        print("\n🎯 Тестируем API рекомендаций...")
        response = requests.get("http://localhost:8000/api/recommendations/resume/1")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API работает! Получено {len(data)} рекомендаций")
            for i, rec in enumerate(data, 1):
                print(f"   {i}. {rec['vacancy_title']} - {rec['company_name']} ({rec['score']:.1%})")
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            print(f"Ответ: {response.text}")
        
        # Тестируем список вакансий
        print("\n📋 Тестируем список вакансий...")
        response = requests.get("http://localhost:8000/api/vacancies")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Список вакансий: {len(data)} вакансий")
            for vacancy in data:
                print(f"   - {vacancy['title']} ({vacancy['company_name']})")
        else:
            print(f"❌ Ошибка списка вакансий: {response.status_code}")
        
        # Тестируем список навыков
        print("\n🛠️ Тестируем список навыков...")
        response = requests.get("http://localhost:8000/api/skills")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Список навыков: {len(data)} навыков")
            for skill in data:
                print(f"   - {skill['name']} ({skill['category']})")
        else:
            print(f"❌ Ошибка списка навыков: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к серверу. Убедитесь, что main.py запущен.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_api()
