"""
REST API для анализа клиентов и генерации уведомлений
"""

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from flask_cors import CORS
from typing import Dict, List, Any
import json
import random
import psycopg2
from datetime import datetime, timedelta

from ..notifications import NotificationPipeline
from .database_managers import MockDatabaseManager, RealDatabaseManager
from .analyzer import analyze_client_with_scenarios


app = Flask(__name__)

# Настройка CORS
CORS(app)

# Настройка Swagger
api = Api(
    app,
    version='1.0',
    title='Push Analytics API',
    description='API для анализа клиентов и генерации персонализированных уведомлений',
    doc='/swagger/'
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
ns = Namespace('api', description='Операции анализа клиентов', path='/api/v1')
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
    @ns.doc(tags=['Система'])
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
    @ns.doc(tags=['Анализ'])
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
    @ns.doc(tags=['Анализ'])
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
                        'score': n.get('score', n.get('analysis_score', 0)),
                        'expected_benefit': n.get('expected_benefit', 0),
                        'priority': n.get('priority', 'low')
                    }
                    for n in top_recommendations
                ]
            }
            
        except Exception as e:
            return {'error': f'Ошибка обработки запроса: {str(e)}'}, 500


@ns.route('/test/db-status')
class TestDatabaseStatus(Resource):
    @ns.doc(tags=['Тестирование'])
    def get(self):
        """
        Проверка статуса подключения к базе данных
        """
        try:
            print("🔍 Проверяем подключение к БД...")
            
            db_manager = RealDatabaseManager()
            
            if not db_manager.connection:
                return {
                    'status': 'error',
                    'message': 'Не удалось подключиться к базе данных',
                    'connected': False
                }, 500
            
            # Проверяем количество клиентов
            try:
                with db_manager.connection.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM \"Clients\"")
                    client_count = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT COUNT(*) FROM \"Transactions\"")
                    transaction_count = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT COUNT(*) FROM \"Transfers\"")
                    transfer_count = cursor.fetchone()[0]
                
                db_manager.close()
                
                return {
                    'status': 'success',
                    'message': 'Подключение к БД установлено',
                    'connected': True,
                    'clients_count': client_count,
                    'transactions_count': transaction_count,
                    'transfers_count': transfer_count
                }
                
            except Exception as e:
                db_manager.close()
                return {
                    'status': 'error',
                    'message': f'Ошибка выполнения запросов: {str(e)}',
                    'connected': False
                }, 500
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Ошибка подключения: {str(e)}',
                'connected': False
            }, 500


@ns.route('/test/random')
class TestRandomClient(Resource):
    @ns.marshal_with(all_analysis_response_model, code=200)
    @ns.marshal_with(error_model, code=400)
    @ns.marshal_with(error_model, code=500)
    @ns.doc(tags=['Тестирование'])
    def get(self):
        """
        Тестовый эндпоинт для анализа случайного клиента из БД
        
        Анализирует поведение случайного клиента по данным за 3 месяца,
        вычисляет ожидаемую выгоду для клиента по каждому продукту,
        выбирает самые полезные продукты,
        генерирует персонализированные push-уведомления в корректном тоне (TOV).
        """
        try:
            print("🔍 Начинаем анализ случайного клиента...")
            
            # Создаем реальный менеджер БД
            db_manager = RealDatabaseManager()
            
            if not db_manager.connection:
                print("❌ Не удалось подключиться к БД")
                return {'error': 'Не удалось подключиться к базе данных'}, 500
            
            print("✅ Подключение к БД установлено")
            
            # Получаем случайного клиента
            client_code = db_manager.get_random_client_code()
            if not client_code:
                print("❌ Клиенты не найдены")
                db_manager.close()
                return {'error': 'Не найдено клиентов в базе данных'}, 400
            
            print(f"🎯 Анализируем случайного клиента: {client_code}")
            
            # Анализируем клиента за 3 месяца (90 дней)
            print("📊 Запускаем анализ сценариев...")
            try:
                notifications = analyze_client_with_scenarios(client_code, 90, db_manager)
                print(f"✅ analyze_client_with_scenarios завершена успешно")
            except Exception as e:
                print(f"❌ ОШИБКА в analyze_client_with_scenarios: {e}")
                import traceback
                traceback.print_exc()
                notifications = []
            
            print(f"📈 Получено уведомлений: {len(notifications) if notifications else 'None'}")
            
            if notifications is None:
                print("❌ notifications is None")
                db_manager.close()
                return {'client_code': int(client_code), 'recommendations': []}
            
            if not notifications:
                print("⚠️  Нет рекомендаций для клиента")
                db_manager.close()
                return {'client_code': int(client_code), 'recommendations': []}
            
            # Возвращаем топ-3 рекомендации
            top_recommendations = notifications[:3]
            print(f"🏆 Топ-3 рекомендации: {len(top_recommendations)}")
            
            # Создаем рекомендации
            print(f"🔍 Создаем рекомендации из {len(top_recommendations)} уведомлений...")
            
            try:
                recommendations = []
                for i, n in enumerate(top_recommendations):
                    rec = {
                        'product': n.get('product_name', ''),
                        'push_notification': n.get('message', ''),
                        'score': n.get('score', n.get('analysis_score', 0)),
                        'expected_benefit': n.get('expected_benefit', 0),
                        'priority': n.get('priority', 'low')
                    }
                    recommendations.append(rec)
                
                print(f"✅ Создано рекомендаций: {len(recommendations)}")
            except Exception as e:
                print(f"❌ ОШИБКА при создании рекомендаций: {e}")
                import traceback
                traceback.print_exc()
                recommendations = []
            
            # Создаем финальный результат
            try:
                client_code_int = int(client_code)
            except Exception as e:
                print(f"❌ Ошибка преобразования client_code: {e}")
                client_code_int = 0
            
            result = {
                'client_code': client_code_int,
                'recommendations': recommendations
            }
            
            print(f"📊 ФИНАЛЬНЫЙ РЕЗУЛЬТАТ: client_code={result['client_code']}, recommendations={len(result['recommendations'])}")
            
            # Закрываем соединение
            db_manager.close()
            print("✅ Анализ завершен успешно")
            
            return result
            
        except Exception as e:
            print(f"❌ Ошибка в основном API endpoint: {str(e)}")
            print(f"❌ Тип ошибки: {type(e).__name__}")
            import traceback
            print(f"❌ Полный traceback:")
            traceback.print_exc()
            print(f"❌ Возвращаем ошибку вместо null")
            return {'error': f'Ошибка обработки запроса: {str(e)}'}, 500


@ns.route('/test/client/<int:client_code>')
class TestSpecificClient(Resource):
    @ns.marshal_with(all_analysis_response_model, code=200)
    @ns.marshal_with(error_model, code=400)
    @ns.marshal_with(error_model, code=500)
    @ns.doc(tags=['Тестирование'])
    def get(self, client_code):
        """
        Тестовый эндпоинт для анализа конкретного клиента из БД
        
        Анализирует поведение указанного клиента по данным за 3 месяца,
        вычисляет ожидаемую выгоду для клиента по каждому продукту,
        выбирает самые полезные продукты,
        генерирует персонализированные push-уведомления в корректном тоне (TOV).
        """
        try:
            # Создаем реальный менеджер БД
            db_manager = RealDatabaseManager()
            
            if not db_manager.connection:
                return {'error': 'Не удалось подключиться к базе данных'}, 500
            
            # Проверяем существование клиента
            client_info = db_manager.get_client_by_code(str(client_code))
            if not client_info:
                db_manager.close()
                return {'error': f'Клиент с кодом {client_code} не найден'}, 400
            
            print(f"🎯 Анализируем клиента: {client_code} ({client_info.get('name', 'Неизвестно')})")
            
            # Анализируем клиента за 3 месяца (90 дней)
            try:
                print(f"🚀 Анализ клиента {client_code}...")
                notifications = analyze_client_with_scenarios(str(client_code), 90, db_manager)
                print(f"🚀 Результат: {len(notifications)} уведомлений")
            except Exception as e:
                print(f"❌ ОШИБКА анализа: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
                notifications = []
            
            # Закрываем соединение
            db_manager.close()
            
            # Подготавливаем результат
            if not notifications:
                print("⚠️ Нет уведомлений")
                return {
                    'client_code': int(client_code),
                    'recommendations': []
                }
            
            # Возвращаем топ-3 рекомендации
            top_recommendations = notifications[:3]
            
            result = {
                'client_code': int(client_code),
                'recommendations': [
                    {
                        'product': n.get('product_name', 'Неизвестный продукт'),
                        'push_notification': n.get('message', 'Сообщение не сгенерировано'),
                        'score': float(n.get('score', n.get('analysis_score', 0))),
                        'expected_benefit': float(n.get('expected_benefit', 0)),
                        'priority': n.get('priority', 'low')
                    }
                    for n in top_recommendations
                ]
            }
            
            print(f"✅ Готово: {len(result['recommendations'])} рекомендаций")
            return result
            
        except Exception as e:
            return {'error': f'Ошибка обработки запроса: {str(e)}'}, 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
