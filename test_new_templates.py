#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест новых шаблонов уведомлений
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from notifications.message_templates import MessageTemplates
from notifications.scenario_integration import ScenarioIntegration
from datetime import datetime

def test_new_templates():
    """Тестирование новых шаблонов сообщений"""
    
    print("🧪 Тестирование новых шаблонов уведомлений")
    print("=" * 50)
    
    templates = MessageTemplates()
    integration = ScenarioIntegration()
    
    # Тестовые данные клиента
    client_data = {
        'client_info': {
            'name': 'Айдар',
            'status': 'зарплатный',
            'avg_monthly_balance_KZT': 1500000
        }
    }
    
    # Тестовые результаты сценариев
    scenario_results = [
        {
            'product_name': 'Карта для путешествий',
            'score': 0.85,
            'expected_benefit': 5000,
            'reasons': ['Много поездок на такси', 'Активные траты на транспорт'],
            'travel_data': {
                'trip_count': 12,
                'travel_amount': 45000,
                'potential_cashback': 2250
            }
        },
        {
            'product_name': 'Премиальная карта',
            'score': 0.75,
            'expected_benefit': 30000,
            'reasons': ['Крупный остаток', 'Траты в ресторанах']
        },
        {
            'product_name': 'Кредитная карта',
            'score': 0.65,
            'expected_benefit': 8000,
            'reasons': ['Активные онлайн-покупки', 'Подписки на сервисы']
        },
        {
            'product_name': 'Доставка еды',
            'score': 0.70,
            'expected_benefit': 1500,
            'reasons': ['Рост трат на доставку', 'Регулярные заказы']
        },
        {
            'product_name': 'Подписки',
            'score': 0.60,
            'expected_benefit': 2000,
            'reasons': ['Множественные подписки', 'Онлайн-сервисы']
        }
    ]
    
    print(f"👤 Клиент: {client_data['client_info']['name']}")
    print(f"💰 Средний баланс: {templates.format_amount(client_data['client_info']['avg_monthly_balance_KZT'])}")
    print()
    
    # Тестируем каждый шаблон
    for i, scenario_result in enumerate(scenario_results, 1):
        print(f"📝 Тест {i}: {scenario_result['product_name']}")
        print("-" * 30)
        
        try:
            # Генерируем уведомление
            notification = integration.generate_notification_from_scenario(
                client_data, scenario_result, scenario_result['product_name']
            )
            
            print(f"✅ Сообщение: {notification['message']}")
            print(f"📊 Длина: {notification['length']} символов")
            print(f"🎯 Приоритет: {notification['priority']}")
            print(f"📱 Каналы: {', '.join(notification['channels'])}")
            print(f"🎨 Персонализация: {notification['personalization']}")
            
            # Проверяем TOV требования
            message = notification['message']
            issues = []
            
            # Проверка длины
            if len(message) < 50 or len(message) > 220:
                issues.append(f"Неправильная длина: {len(message)}")
            
            # Проверка КАПС
            if message.isupper():
                issues.append("Есть КАПС")
            
            # Проверка восклицательных знаков
            if message.count('!') > 1:
                issues.append("Слишком много восклицательных знаков")
            
            # Проверка форматирования валюты
            if '₸' in message and ' ₸' not in message:
                issues.append("Неправильное форматирование валюты")
            
            if issues:
                print(f"⚠️  Проблемы: {', '.join(issues)}")
            else:
                print("✅ TOV требования соблюдены")
                
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        
        print()
    
    print("🎯 Тестирование форматирования сумм")
    print("-" * 30)
    
    test_amounts = [1000, 50000, 1500000, 5000000]
    for amount in test_amounts:
        formatted = templates.format_amount(amount)
        print(f"{amount:>10} → {formatted}")
    
    print()
    print("📅 Тестирование форматирования дат")
    print("-" * 30)
    
    test_date = datetime.now()
    formatted_date = templates.format_date(test_date)
    print(f"Текущая дата: {formatted_date}")
    
    print()
    print("✅ Тестирование завершено!")

if __name__ == "__main__":
    test_new_templates()
