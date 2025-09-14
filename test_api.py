#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API
"""

import requests
import json

# Базовый URL API
BASE_URL = "http://localhost:7778"

def test_health():
    """Тест health check endpoint"""
    print("🔍 Тестируем health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analytics/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_analyze():
    """Тест анализа клиента"""
    print("\n🔍 Тестируем анализ клиента...")
    
    test_data = {
        "client_code": 1,
        "name": "Рамазан",
        "status": "Зарплатный клиент",
        "avg_monthly_balance_KZT": 240000,
        "city": "Алматы",
        "age": 30,
        "transactions": [
            {"date": "2025-08-10", "category": "Такси", "amount": 27400, "currency": "KZT"},
            {"date": "2025-08-12", "category": "Продукты питания", "amount": 44000, "currency": "KZT"}
        ],
        "transfers": [
            {"date": "2025-08-01", "type": "salary_in", "direction": "in", "amount": 320000, "currency": "KZT"}
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/analytics/analyze",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_analyze_all():
    """Тест анализа всех продуктов"""
    print("\n🔍 Тестируем анализ всех продуктов...")
    
    test_data = {
        "client_code": 1,
        "name": "Рамазан",
        "status": "Зарплатный клиент",
        "avg_monthly_balance_KZT": 240000,
        "city": "Алматы",
        "age": 30,
        "transactions": [
            {"date": "2025-08-10", "category": "Такси", "amount": 27400, "currency": "KZT"},
            {"date": "2025-08-12", "category": "Продукты питания", "amount": 44000, "currency": "KZT"}
        ],
        "transfers": [
            {"date": "2025-08-01", "type": "salary_in", "direction": "in", "amount": 320000, "currency": "KZT"}
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/analytics/analyze/all",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов API...")
    print(f"Base URL: {BASE_URL}")
    
    tests = [
        ("Health Check", test_health),
        ("Analyze Client", test_analyze),
        ("Analyze All Products", test_analyze_all)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Тест: {test_name}")
        print('='*50)
        result = test_func()
        results.append((test_name, result))
    
    print(f"\n{'='*50}")
    print("РЕЗУЛЬТАТЫ ТЕСТОВ")
    print('='*50)
    
    for test_name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nИтого: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены успешно!")
    else:
        print("⚠️  Некоторые тесты провалены")

if __name__ == "__main__":
    main()
