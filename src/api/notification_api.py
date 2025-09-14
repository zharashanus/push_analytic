"""
REST API для анализа клиентов и генерации уведомлений
"""

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
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

# Настройка Swagger
api = Api(
    app,
    version='1.0',
    title='Push Analytics API',
    description='API для анализа клиентов и генерации персонализированных уведомлений',
    doc='/swagger/',
    prefix='/api/v1'
)

# Добавляем маршруты для swagger.json
@app.route('/swagger.json')
def swagger_json():
    """Swagger JSON definition"""
    return api.__schema__

@app.route('/api/v1/swagger.json')
def api_swagger_json():
    """API Swagger JSON definition"""
    return api.__schema__

# Создаем namespace для API
ns = Namespace('', description='Операции анализа клиентов')
api.add_namespace(ns)

# Модели данных для Swagger
client_model = api.model('Client', {
    'client_code': fields.Integer(required=True, description='Код клиента'),
    'name': fields.String(required=True, description='Имя клиента'),
    'status': fields.String(required=True, description='Статус клиента'),
    'avg_monthly_balance_KZT': fields.Float(required=True, description='Средний месячный баланс в тенге'),
    'city': fields.String(description='Город клиента'),
    'age': fields.Integer(description='Возраст клиента'),
    'transactions': fields.List(fields.Raw, description='Список транзакций'),
    'transfers': fields.List(fields.Raw, description='Список переводов')
})

transaction_model = api.model('Transaction', {
    'date': fields.String(required=True, description='Дата транзакции'),
    'category': fields.String(required=True, description='Категория транзакции'),
    'amount': fields.Float(required=True, description='Сумма транзакции'),
    'currency': fields.String(required=True, description='Валюта транзакции')
})

transfer_model = api.model('Transfer', {
    'date': fields.String(required=True, description='Дата перевода'),
    'type': fields.String(required=True, description='Тип перевода'),
    'direction': fields.String(required=True, description='Направление перевода'),
    'amount': fields.Float(required=True, description='Сумма перевода'),
    'currency': fields.String(required=True, description='Валюта перевода')
})

analysis_response_model = api.model('AnalysisResponse', {
    'client_code': fields.Integer(description='Код клиента'),
    'product': fields.String(description='Рекомендуемый продукт'),
    'push_notification': fields.String(description='Текст push-уведомления')
})

recommendation_model = api.model('Recommendation', {
    'product': fields.String(description='Название продукта'),
    'push_notification': fields.String(description='Текст push-уведомления'),
    'score': fields.Float(description='Скор продукта'),
    'expected_benefit': fields.Float(description='Ожидаемая выгода'),
    'priority': fields.String(description='Приоритет рекомендации')
})

all_analysis_response_model = api.model('AllAnalysisResponse', {
    'client_code': fields.Integer(description='Код клиента'),
    'recommendations': fields.List(fields.Nested(recommendation_model), description='Список рекомендаций')
})

error_model = api.model('Error', {
    'error': fields.String(description='Описание ошибки')
})

# Инициализируем пайплайн
pipeline = NotificationPipeline()


@ns.route('/health')
class HealthCheck(Resource):
    def get(self):
        """
        Health check endpoint
        
        Проверяет работоспособность API
        """
        return {'status': 'healthy', 'service': 'push_analytics'}, 200


@ns.route('/analyze')
class AnalyzeClient(Resource):
    @ns.expect(client_model)
    @ns.marshal_with(analysis_response_model, code=200)
    @ns.marshal_with(error_model, code=400)
    @ns.marshal_with(error_model, code=500)
    def post(self):
        """
        Анализ клиента и генерация рекомендаций
        
        Анализирует данные клиента и возвращает лучшую рекомендацию продукта
        с персонализированным push-уведомлением.
        """
        try:
            data = request.get_json()
            
            # Валидируем входные данные
            if not data:
                return {'error': 'Отсутствуют данные'}, 400
            
            required_fields = ['client_code', 'name', 'status', 'avg_monthly_balance_KZT']
            for field in required_fields:
                if field not in data:
                    return {'error': f'Отсутствует обязательное поле: {field}'}, 400
            
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
                return {
                    'client_code': client_code,
                    'product': 'Нет подходящих продуктов',
                    'push_notification': 'У вас пока нет подходящих продуктов. Мы уведомим, когда появятся новые предложения.'
                }
            
            best_notification = notifications[0]
            
            return {
                'client_code': client_code,
                'product': best_notification.get('product_name', ''),
                'push_notification': best_notification.get('message', '')
            }
            
        except Exception as e:
            return {'error': f'Ошибка обработки запроса: {str(e)}'}, 500


@ns.route('/analyze/all')
class AnalyzeClientAll(Resource):
    @ns.expect(client_model)
    @ns.marshal_with(all_analysis_response_model, code=200)
    @ns.marshal_with(error_model, code=400)
    @ns.marshal_with(error_model, code=500)
    def post(self):
        """
        Анализ клиента для всех продуктов
        
        Анализирует данные клиента и возвращает топ-4 рекомендации продуктов
        с персонализированными push-уведомлениями.
        """
        try:
            data = request.get_json()
            
            if not data:
                return {'error': 'Отсутствуют данные'}, 400
            
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
            
            return {
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
            }
            
        except Exception as e:
            return {'error': f'Ошибка обработки запроса: {str(e)}'}, 500


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