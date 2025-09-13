from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
import os
from datetime import datetime
import pandas as pd
import numpy as np

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Import models after db initialization
from models import Client, Transaction, Transfer, ProductBenefit

# Product definitions and templates
PRODUCTS = {
    "Карта для путешествий": {
        "cashback_rate": 0.04,  # 4% кэшбэк
        "categories": ["Такси", "Отели", "Авиабилеты", "Рестораны"],
        "min_balance": 0,
        "template": "{name}, в {month} вы сделали {count} поездок на такси на {amount} ₸. С картой для путешествий вернули бы ≈{benefit} ₸. Откройте карту."
    },
    "Премиальная карта": {
        "cashback_rate": 0.05,  # 5% кэшбэк
        "categories": ["Все категории"],
        "min_balance": 6000000,  # 6 млн тенге
        "template": "{name}, с вашим балансом {balance} ₸ премиальная карта даст до {benefit} ₸ кэшбэка в месяц. Оформите сейчас."
    },
    "Депозит": {
        "interest_rate": 0.12,  # 12% годовых
        "min_balance": 1000000,  # 1 млн тенге
        "template": "{name}, с вашим балансом {balance} ₸ депозит принесет {benefit} ₸ в год. Откройте депозит."
    },
    "Кредитная карта": {
        "credit_limit_multiplier": 0.3,  # 30% от баланса
        "categories": ["Продукты питания", "Транспорт", "Развлечения"],
        "template": "{name}, кредитная карта с лимитом {limit} ₸ поможет в непредвиденных ситуациях. Оформите за 5 минут."
    },
    "Обмен валют": {
        "fx_categories": ["Обмен валют", "Международные переводы"],
        "template": "{name}, вы часто меняете валюту. Наш курс выгоднее на 0.5%. Экономьте на каждой операции."
    }
}

def analyze_client_data(client_data):
    """Анализирует данные клиента и возвращает лучший продукт с пуш-уведомлением"""
    
    client_code = client_data['client_code']
    name = client_data['name']
    avg_balance = client_data.get('avg_monthly_balance_KZT', 0)
    transactions = client_data.get('transactions', [])
    transfers = client_data.get('transfers', [])
    
    # Анализ транзакций
    transaction_df = pd.DataFrame(transactions)
    if not transaction_df.empty:
        transaction_df['amount'] = pd.to_numeric(transaction_df['amount'])
        transaction_df['date'] = pd.to_datetime(transaction_df['date'])
        
        # Группировка по категориям
        category_spending = transaction_df.groupby('category')['amount'].sum().sort_values(ascending=False)
        
        # Анализ по месяцам
        transaction_df['month'] = transaction_df['date'].dt.to_period('M')
        monthly_spending = transaction_df.groupby('month')['amount'].sum()
        
        # Топ категории
        top_categories = category_spending.head(3).to_dict()
    else:
        top_categories = {}
        monthly_spending = {}
    
    # Анализ переводов
    transfer_df = pd.DataFrame(transfers)
    if not transfer_df.empty:
        transfer_df['amount'] = pd.to_numeric(transfer_df['amount'])
        salary_transfers = transfer_df[transfer_df['type'] == 'salary_in']['amount'].sum()
    else:
        salary_transfers = 0
    
    # Расчет выгоды по продуктам
    product_benefits = {}
    
    # Карта для путешествий
    taxi_spending = top_categories.get('Такси', 0)
    if taxi_spending > 0:
        benefit = taxi_spending * PRODUCTS["Карта для путешествий"]["cashback_rate"]
        product_benefits["Карта для путешествий"] = {
            "benefit": benefit,
            "data": {
                "taxi_count": len(transaction_df[transaction_df['category'] == 'Такси']),
                "taxi_amount": taxi_spending,
                "month": datetime.now().strftime("%B")
            }
        }
    
    # Премиальная карта
    if avg_balance >= PRODUCTS["Премиальная карта"]["min_balance"]:
        monthly_spending_total = sum(monthly_spending.values()) if monthly_spending else 0
        benefit = monthly_spending_total * PRODUCTS["Премиальная карта"]["cashback_rate"]
        product_benefits["Премиальная карта"] = {
            "benefit": benefit,
            "data": {"balance": avg_balance}
        }
    
    # Депозит
    if avg_balance >= PRODUCTS["Депозит"]["min_balance"]:
        benefit = avg_balance * PRODUCTS["Депозит"]["interest_rate"]
        product_benefits["Депозит"] = {
            "benefit": benefit,
            "data": {"balance": avg_balance}
        }
    
    # Кредитная карта
    if avg_balance > 0:
        credit_limit = avg_balance * PRODUCTS["Кредитная карта"]["credit_limit_multiplier"]
        product_benefits["Кредитная карта"] = {
            "benefit": 0,  # Нет прямой выгоды, но есть удобство
            "data": {"limit": credit_limit}
        }
    
    # Обмен валют
    fx_spending = top_categories.get('Обмен валют', 0)
    if fx_spending > 0:
        benefit = fx_spending * 0.005  # 0.5% экономии
        product_benefits["Обмен валют"] = {
            "benefit": benefit,
            "data": {"fx_amount": fx_spending}
        }
    
    # Выбор лучшего продукта
    if not product_benefits:
        # Если нет подходящих продуктов, предлагаем дефолтный
        best_product = "Кредитная карта"
        push_text = f"{name}, откройте кредитную карту для удобных покупок."
    else:
        best_product = max(product_benefits.keys(), key=lambda x: product_benefits[x]["benefit"])
        best_data = product_benefits[best_product]
        
        # Генерация текста пуша
        template = PRODUCTS[best_product]["template"]
        push_text = template.format(
            name=name,
            **best_data["data"],
            benefit=int(best_data["benefit"]),
            balance=f"{avg_balance:,.0f}".replace(",", " ")
        )
    
    return {
        "client_code": client_code,
        "product": best_product,
        "push_notification": push_text
    }

@app.route('/analyze', methods=['POST'])
def analyze():
    """Основной эндпоинт для анализа данных клиента"""
    try:
        data = request.get_json()
        
        # Валидация входных данных
        required_fields = ['client_code', 'name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Анализ данных
        result = analyze_client_data(data)
        
        # Сохранение в базу данных
        try:
            # Сохраняем клиента
            client = Client.query.filter_by(client_code=data['client_code']).first()
            if not client:
                client = Client(
                    client_code=data['client_code'],
                    name=data['name'],
                    status=data.get('status', 'Обычный клиент'),
                    avg_monthly_balance=data.get('avg_monthly_balance_KZT', 0)
                )
                db.session.add(client)
            
            # Сохраняем транзакции
            for trans in data.get('transactions', []):
                transaction = Transaction(
                    client_code=data['client_code'],
                    date=datetime.strptime(trans['date'], '%Y-%m-%d'),
                    category=trans['category'],
                    amount=trans['amount'],
                    currency=trans['currency']
                )
                db.session.add(transaction)
            
            # Сохраняем переводы
            for transfer in data.get('transfers', []):
                transfer_obj = Transfer(
                    client_code=data['client_code'],
                    date=datetime.strptime(transfer['date'], '%Y-%m-%d'),
                    type=transfer['type'],
                    direction=transfer['direction'],
                    amount=transfer['amount'],
                    currency=transfer['currency']
                )
                db.session.add(transfer_obj)
            
            # Сохраняем результат анализа
            product_benefit = ProductBenefit(
                client_code=data['client_code'],
                product=result['product'],
                expected_benefit=0  # Будет рассчитано в анализе
            )
            db.session.add(product_benefit)
            
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            print(f"Database error: {e}")
            # Продолжаем выполнение даже если БД недоступна
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Проверка здоровья сервиса"""
    return jsonify({'status': 'healthy', 'service': 'push_analytic'})

@app.route('/', methods=['GET'])
def index():
    """Главная страница"""
    return jsonify({
        'service': 'push_analytic',
        'version': '1.0.0',
        'endpoints': {
            'POST /analyze': 'Анализ данных клиента и генерация пуш-уведомления',
            'GET /health': 'Проверка здоровья сервиса'
        }
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
