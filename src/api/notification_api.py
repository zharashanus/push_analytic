"""
REST API для анализа клиентов и генерации уведомлений
"""

from flask import Flask, request, jsonify
from typing import Dict, List, Any
import json
from datetime import datetime

from ..notifications import NotificationPipeline
from ..products import (
    TravelCardScenario, PremiumCardScenario, CreditCardScenario,
    CurrencyExchangeScenario, MultiCurrencyDepositScenario,
    SavingsDepositScenario, AccumulationDepositScenario,
    InvestmentsScenario, GoldBarsScenario, CashCreditScenario
)


app = Flask(__name__)

# Инициализируем пайплайн
pipeline = NotificationPipeline()


@app.route('/analyze', methods=['POST'])
def analyze_client():
    """
    Анализ клиента и генерация рекомендаций
    
    Пример запроса:
    {
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
    """
    try:
        data = request.get_json()
        
        # Валидируем входные данные
        if not data:
            return jsonify({'error': 'Отсутствуют данные'}), 400
        
        required_fields = ['client_code', 'name', 'status', 'avg_monthly_balance_KZT']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Отсутствует обязательное поле: {field}'}), 400
        
        # Создаем мок-данные для анализа (в реальности используем БД)
        client_code = data['client_code']
        client_info = {
            'client_code': client_code,
            'name': data['name'],
            'status': data['status'],
            'avg_monthly_balance_KZT': data['avg_monthly_balance_KZT'],
            'city': data.get('city', 'Алматы'),
            'age': data.get('age', 30)
        }
        
        transactions = data.get('transactions', [])
        transfers = data.get('transfers', [])
        
        # Создаем мок-менеджер БД
        mock_db_manager = MockDatabaseManager(client_info, transactions, transfers)
        
        # Анализируем клиента
        notifications = analyze_client_with_scenarios(client_code, 90, mock_db_manager)
        
        # Получаем лучшую рекомендацию
        if not notifications:
            return jsonify({
                'client_code': client_code,
                'product': 'Нет подходящих продуктов',
                'push_notification': 'У вас пока нет подходящих продуктов. Мы уведомим, когда появятся новые предложения.'
            })
        
        best_notification = notifications[0]
        
        return jsonify({
            'client_code': client_code,
            'product': best_notification.get('product_name', ''),
            'push_notification': best_notification.get('message', ''),
            'score': best_notification.get('analysis_score', 0),
            'expected_benefit': best_notification.get('expected_benefit', 0),
            'priority': best_notification.get('priority', 'low')
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка обработки запроса: {str(e)}'}), 500


@app.route('/analyze/all', methods=['POST'])
def analyze_client_all():
    """Анализ клиента для всех продуктов"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Отсутствуют данные'}), 400
        
        client_code = data['client_code']
        client_info = {
            'client_code': client_code,
            'name': data['name'],
            'status': data['status'],
            'avg_monthly_balance_KZT': data['avg_monthly_balance_KZT'],
            'city': data.get('city', 'Алматы'),
            'age': data.get('age', 30)
        }
        
        transactions = data.get('transactions', [])
        transfers = data.get('transfers', [])
        
        mock_db_manager = MockDatabaseManager(client_info, transactions, transfers)
        notifications = analyze_client_with_scenarios(client_code, 90, mock_db_manager)
        
        # Возвращаем топ-4 рекомендации
        top_recommendations = notifications[:4]
        
        return jsonify({
            'client_code': client_code,
            'recommendations': [
                {
                    'product': n.get('product_name', ''),
                    'push_notification': n.get('message', ''),
                    'score': n.get('analysis_score', 0),
                    'expected_benefit': n.get('expected_benefit', 0),
                    'priority': n.get('priority', 'low')
                }
                for n in top_recommendations
            ]
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка обработки запроса: {str(e)}'}), 500


def analyze_client_with_scenarios(client_code: str, days: int, db_manager) -> List[Dict[str, Any]]:
    """Анализ клиента с использованием всех сценариев"""
    from ..notifications.scenario_integration import ScenarioIntegration
    
    integration = ScenarioIntegration()
    notifications = []
    
    scenarios = {
        'travel_card': TravelCardScenario(),
        'premium_card': PremiumCardScenario(),
        'credit_card': CreditCardScenario(),
        'currency_exchange': CurrencyExchangeScenario(),
        'multi_currency_deposit': MultiCurrencyDepositScenario(),
        'savings_deposit': SavingsDepositScenario(),
        'accumulation_deposit': AccumulationDepositScenario(),
        'investments': InvestmentsScenario(),
        'gold_bars': GoldBarsScenario(),
        'cash_credit': CashCreditScenario()
    }
    
    for product_key, scenario in scenarios.items():
        try:
            # Анализируем клиента
            scenario_result = scenario.analyze_client(client_code, days, db_manager)
            
            # Получаем данные клиента
            client_data = scenario.get_client_data(client_code, days, db_manager)
            
            # Генерируем уведомление
            notification = integration.generate_notification_from_scenario(
                client_data, scenario_result, scenario.product_name
            )
            
            notification.update({
                'client_code': client_code,
                'product_key': product_key,
                'analysis_score': scenario_result.get('score', 0),
                'expected_benefit': scenario_result.get('expected_benefit', 0)
            })
            
            notifications.append(notification)
            
        except Exception as e:
            print(f"Ошибка анализа продукта {product_key}: {e}")
            continue
    
    # Сортируем по приоритету и скорингу
    notifications.sort(key=lambda x: (x['priority'], x['analysis_score']), reverse=True)
    
    return notifications


class MockDatabaseManager:
    """Мок-менеджер базы данных для тестирования"""
    
    def __init__(self, client_info: Dict, transactions: List[Dict], transfers: List[Dict]):
        self.client_info = client_info
        self.transactions = transactions
        self.transfers = transfers
    
    def get_client_by_code(self, client_code: str) -> Dict:
        """Получить данные клиента"""
        if str(self.client_info['client_code']) == str(client_code):
            return self.client_info
        return {}
    
    def execute_query(self, query: str, params: tuple) -> List[Dict]:
        """Выполнить SQL запрос"""
        if 'Transactions' in query:
            return self.transactions
        elif 'Transfers' in query:
            return self.transfers
        return []


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
