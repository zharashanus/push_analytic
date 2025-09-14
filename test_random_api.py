#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API /api/v1/test/random
"""

import requests
import json

# Базовый URL API
BASE_URL = "http://localhost:7778"

def test_random_client():
    """Тест анализа случайного клиента"""
    print("🔍 Тестируем анализ случайного клиента...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/test/random")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n🔍 Анализ ответа:")
            print(f"  - client_code: {data.get('client_code')} (тип: {type(data.get('client_code'))})")
            print(f"  - recommendations: {data.get('recommendations')} (тип: {type(data.get('recommendations'))})")
            
            if data.get('recommendations') is not None:
                print(f"  - Количество рекомендаций: {len(data.get('recommendations', []))}")
                if data.get('recommendations'):
                    print(f"  - Первая рекомендация: {data.get('recommendations')[0]}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск теста API /api/v1/test/random...")
    print(f"Base URL: {BASE_URL}")
    
    result = test_random_client()
    
    print(f"\n{'='*50}")
    print("РЕЗУЛЬТАТ ТЕСТА")
    print('='*50)
    
    status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
    print(f"Test Random Client: {status}")

if __name__ == "__main__":
    main()
