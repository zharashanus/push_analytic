"""
Тестовый скрипт для проверки интеграции сценариев и уведомлений
"""

import json
from src.notifications import NotificationPipeline
from src.products import (
    TravelCardScenario, PremiumCardScenario, CreditCardScenario
)


def test_travel_card_scenario():
    """Тест сценария карты путешествий"""
    print("=== Тест карты путешествий ===")
    
    # Создаем тестовые данные
    client_data = {
        'client_info': {
            'client_code': '12345',
            'name': 'Рамазан',
            'status': 'Зарплатный клиент',
            'avg_monthly_balance_KZT': 240000,
            'city': 'Алматы'
        },
        'transactions': [
            {'date': '2025-08-10', 'category': 'Такси', 'amount': 27400, 'currency': 'KZT'},
            {'date': '2025-08-12', 'category': 'Отели', 'amount': 150000, 'currency': 'KZT'},
            {'date': '2025-08-15', 'category': 'Путешествия', 'amount': 80000, 'currency': 'KZT'},
            {'date': '2025-08-20', 'category': 'Такси', 'amount': 12000, 'currency': 'KZT'}
        ],
        'transfers': [
            {'date': '2025-08-01', 'type': 'salary_in', 'direction': 'in', 'amount': 320000, 'currency': 'KZT'}
        ]
    }
    
    # Создаем мок-менеджер БД
    class MockDBManager:
        def get_client_by_code(self, client_code):
            return client_data['client_info']
        
        def execute_query(self, query, params):
            if 'Transactions' in query:
                return client_data['transactions']
            elif 'Transfers' in query:
                return client_data['transfers']
            return []
    
    db_manager = MockDBManager()
    
    # Тестируем сценарий
    scenario = TravelCardScenario()
    result = scenario.analyze_client('12345', 90, db_manager)
    
    print(f"Скор: {result['score']:.2f}")
    print(f"Причины: {result['reasons']}")
    print(f"Ожидаемая выгода: {result['expected_benefit']:.2f} ₸")
    
    # Тестируем генерацию уведомления
    from src.notifications.scenario_integration import ScenarioIntegration
    integration = ScenarioIntegration()
    
    notification = integration.generate_notification_from_scenario(
        client_data, result, scenario.product_name
    )
    
    print(f"Уведомление: {notification['message']}")
    print(f"Приоритет: {notification['priority']}")
    print(f"Длина: {notification['length']} символов")
    print()


def test_premium_card_scenario():
    """Тест сценария премиальной карты"""
    print("=== Тест премиальной карты ===")
    
    client_data = {
        'client_info': {
            'client_code': '67890',
            'name': 'Айгуль',
            'status': 'Премиальный клиент',
            'avg_monthly_balance_KZT': 2500000,
            'city': 'Астана'
        },
        'transactions': [
            {'date': '2025-08-10', 'category': 'Кафе и рестораны', 'amount': 150000, 'currency': 'KZT'},
            {'date': '2025-08-12', 'category': 'Косметика и Парфюмерия', 'amount': 80000, 'currency': 'KZT'},
            {'date': '2025-08-15', 'category': 'Ювелирные украшения', 'amount': 300000, 'currency': 'KZT'},
            {'date': '2025-08-20', 'category': 'Подарки', 'amount': 120000, 'currency': 'KZT'}
        ],
        'transfers': [
            {'date': '2025-08-01', 'type': 'salary_in', 'direction': 'in', 'amount': 5000000, 'currency': 'KZT'}
        ]
    }
    
    class MockDBManager:
        def get_client_by_code(self, client_code):
            return client_data['client_info']
        
        def execute_query(self, query, params):
            if 'Transactions' in query:
                return client_data['transactions']
            elif 'Transfers' in query:
                return client_data['transfers']
            return []
    
    db_manager = MockDBManager()
    
    scenario = PremiumCardScenario()
    result = scenario.analyze_client('67890', 90, db_manager)
    
    print(f"Скор: {result['score']:.2f}")
    print(f"Причины: {result['reasons']}")
    print(f"Ожидаемая выгода: {result['expected_benefit']:.2f} ₸")
    
    from src.notifications.scenario_integration import ScenarioIntegration
    integration = ScenarioIntegration()
    
    notification = integration.generate_notification_from_scenario(
        client_data, result, scenario.product_name
    )
    
    print(f"Уведомление: {notification['message']}")
    print(f"Приоритет: {notification['priority']}")
    print(f"Длина: {notification['length']} символов")
    print()


def test_credit_card_scenario():
    """Тест сценария кредитной карты"""
    print("=== Тест кредитной карты ===")
    
    client_data = {
        'client_info': {
            'client_code': '11111',
            'name': 'Данияр',
            'status': 'Стандартный клиент',
            'avg_monthly_balance_KZT': 500000,
            'city': 'Алматы'
        },
        'transactions': [
            {'date': '2025-08-10', 'category': 'Кино', 'amount': 5000, 'currency': 'KZT'},
            {'date': '2025-08-12', 'category': 'Играем дома', 'amount': 15000, 'currency': 'KZT'},
            {'date': '2025-08-15', 'category': 'Смотрим дома', 'amount': 8000, 'currency': 'KZT'},
            {'date': '2025-08-20', 'category': 'Кафе и рестораны', 'amount': 25000, 'currency': 'KZT'},
            {'date': '2025-08-25', 'category': 'Продукты питания', 'amount': 45000, 'currency': 'KZT'}
        ],
        'transfers': [
            {'date': '2025-08-01', 'type': 'salary_in', 'direction': 'in', 'amount': 800000, 'currency': 'KZT'}
        ]
    }
    
    class MockDBManager:
        def get_client_by_code(self, client_code):
            return client_data['client_info']
        
        def execute_query(self, query, params):
            if 'Transactions' in query:
                return client_data['transactions']
            elif 'Transfers' in query:
                return client_data['transfers']
            return []
    
    db_manager = MockDBManager()
    
    scenario = CreditCardScenario()
    result = scenario.analyze_client('11111', 90, db_manager)
    
    print(f"Скор: {result['score']:.2f}")
    print(f"Причины: {result['reasons']}")
    print(f"Ожидаемая выгода: {result['expected_benefit']:.2f} ₸")
    
    from src.notifications.scenario_integration import ScenarioIntegration
    integration = ScenarioIntegration()
    
    notification = integration.generate_notification_from_scenario(
        client_data, result, scenario.product_name
    )
    
    print(f"Уведомление: {notification['message']}")
    print(f"Приоритет: {notification['priority']}")
    print(f"Длина: {notification['length']} символов")
    print()


def test_api_request():
    """Тест API запроса"""
    print("=== Тест API запроса ===")
    
    # Пример запроса как в задании
    request_data = {
        "client_code": 1,
        "name": "Рамазан",
        "status": "Зарплатный клиент",
        "avg_monthly_balance_KZT": 240000,
        "transactions": [
            {"date": "2025-08-10", "category": "Такси", "amount": 27400, "currency": "KZT"},
            {"date": "2025-08-12", "category": "Продукты питания", "amount": 44000, "currency": "KZT"}
        ],
        "transfers": [
            {"date": "2025-08-01", "type": "salary_in", "direction": "in", "amount": 320000, "currency": "KZT"}
        ]
    }
    
    print("Входные данные:")
    print(json.dumps(request_data, ensure_ascii=False, indent=2))
    print()
    
    # Симулируем обработку
    client_data = {
        'client_info': {
            'client_code': request_data['client_code'],
            'name': request_data['name'],
            'status': request_data['status'],
            'avg_monthly_balance_KZT': request_data['avg_monthly_balance_KZT'],
            'city': 'Алматы'
        },
        'transactions': request_data['transactions'],
        'transfers': request_data['transfers']
    }
    
    class MockDBManager:
        def get_client_by_code(self, client_code):
            return client_data['client_info']
        
        def execute_query(self, query, params):
            if 'Transactions' in query:
                return client_data['transactions']
            elif 'Transfers' in query:
                return client_data['transfers']
            return []
    
    db_manager = MockDBManager()
    
    # Тестируем карту путешествий
    scenario = TravelCardScenario()
    result = scenario.analyze_client(1, 90, db_manager)
    
    from src.notifications.scenario_integration import ScenarioIntegration
    integration = ScenarioIntegration()
    
    notification = integration.generate_notification_from_scenario(
        client_data, result, scenario.product_name
    )
    
    response = {
        "client_code": 1,
        "product": notification['product_name'],
        "push_notification": notification['message'],
        "score": notification['analysis_score'],
        "expected_benefit": notification['expected_benefit']
    }
    
    print("Ответ API:")
    print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    print("Тестирование интеграции сценариев и уведомлений\n")
    
    test_travel_card_scenario()
    test_premium_card_scenario()
    test_credit_card_scenario()
    test_api_request()
    
    print("Тестирование завершено!")
