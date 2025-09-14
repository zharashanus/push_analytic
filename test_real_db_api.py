#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API с реальными данными из БД
"""

import requests
import json

# Базовый URL API
BASE_URL = "http://localhost:7778"

def test_health():
    """Тест health check endpoint"""
    print("🔍 Тестируем health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_random_client():
    """Тест анализа случайного клиента из БД"""
    print("\n🔍 Тестируем анализ случайного клиента из БД...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/test/random-client",
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Найден клиент: {data['client_code']}")
            print(f"📊 Количество рекомендаций: {len(data['recommendations'])}")
            
            for i, rec in enumerate(data['recommendations'], 1):
                print(f"\n🏆 Топ-{i}: {rec['product']}")
                print(f"   Скор: {rec['score']:.2f}")
                print(f"   Ожидаемая выгода: {rec['expected_benefit']:,.0f} ₸")
                print(f"   Приоритет: {rec['priority']}")
                print(f"   Уведомление: {rec['push_notification']}")
            
            return True
        else:
            print(f"❌ Ошибка: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_specific_client(client_code):
    """Тест анализа конкретного клиента из БД"""
    print(f"\n🔍 Тестируем анализ клиента {client_code} из БД...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/test/random-client/{client_code}",
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Найден клиент: {data['client_code']}")
            print(f"📊 Количество рекомендаций: {len(data['recommendations'])}")
            
            for i, rec in enumerate(data['recommendations'], 1):
                print(f"\n🏆 Топ-{i}: {rec['product']}")
                print(f"   Скор: {rec['score']:.2f}")
                print(f"   Ожидаемая выгода: {rec['expected_benefit']:,.0f} ₸")
                print(f"   Приоритет: {rec['priority']}")
                print(f"   Уведомление: {rec['push_notification']}")
            
            return True
        else:
            print(f"❌ Ошибка: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_analyze_with_mock_data():
    """Тест анализа с мок-данными (для сравнения)"""
    print("\n🔍 Тестируем анализ с мок-данными...")
    
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
            f"{BASE_URL}/api/v1/analyze/all",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Анализ завершен для клиента: {data['client_code']}")
            print(f"📊 Количество рекомендаций: {len(data['recommendations'])}")
            
            for i, rec in enumerate(data['recommendations'], 1):
                print(f"\n🏆 Топ-{i}: {rec['product']}")
                print(f"   Скор: {rec['score']:.2f}")
                print(f"   Ожидаемая выгода: {rec['expected_benefit']:,.0f} ₸")
                print(f"   Приоритет: {rec['priority']}")
                print(f"   Уведомление: {rec['push_notification']}")
            
            return True
        else:
            print(f"❌ Ошибка: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов API с реальными данными...")
    print(f"Base URL: {BASE_URL}")
    
    tests = [
        ("Health Check", test_health),
        ("Mock Data Analysis", test_analyze_with_mock_data),
        ("Random Client Analysis", test_random_client),
    ]
    
    # Добавляем тест конкретного клиента, если указан
    import sys
    if len(sys.argv) > 1:
        try:
            client_code = int(sys.argv[1])
            tests.append((f"Specific Client {client_code}", lambda: test_specific_client(client_code)))
        except ValueError:
            print(f"⚠️  Неверный код клиента: {sys.argv[1]}")
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Тест: {test_name}")
        print('='*60)
        result = test_func()
        results.append((test_name, result))
    
    print(f"\n{'='*60}")
    print("РЕЗУЛЬТАТЫ ТЕСТОВ")
    print('='*60)
    
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
    
    print(f"\n💡 Использование:")
    print(f"   python {__file__}                    # Тест случайного клиента")
    print(f"   python {__file__} 12345             # Тест конкретного клиента")

if __name__ == "__main__":
    main()
