"""
Анализатор клиентов с использованием сценариев
"""

from typing import Dict, List, Any
import time
from ..products import (
    TravelCardScenario, PremiumCardScenario, CreditCardScenario,
    CurrencyExchangeScenario, MultiCurrencyDepositScenario,
    SavingsDepositScenario, AccumulationDepositScenario,
    InvestmentsScenario, GoldBarsScenario, CashCreditScenario
)


def analyze_client_with_scenarios(client_code: str, days: int, db_manager) -> List[Dict[str, Any]]:
    """Анализ клиента с использованием всех сценариев"""
    from ..notifications.scenario_integration import ScenarioIntegration
    
    print(f"🔍 Анализ клиента {client_code} за {days} дней")
    start_time = time.time()
    
    try:
        integration = ScenarioIntegration()
        notifications = []
    except Exception as e:
        print(f"❌ Ошибка инициализации ScenarioIntegration: {e}")
        return []
    
    try:
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
    except Exception as e:
        print(f"❌ Ошибка создания сценариев: {e}")
        return []
    
    print(f"📊 Доступно сценариев: {len(scenarios)}")
    print(f"🔍 Список сценариев: {list(scenarios.keys())}")
    
    for product_key, scenario in scenarios.items():
        try:
            # Проверяем таймаут (максимум 30 секунд)
            if time.time() - start_time > 30:
                print(f"⏰ Таймаут анализа достигнут, завершаем с {len(notifications)} уведомлениями")
                break
                
            print(f"🔍 {product_key}...", end=" ")
            
            # Анализируем клиента
            print(f"🔧 Анализируем сценарий {product_key}...")
            scenario_result = scenario.analyze_client(client_code, days, db_manager)
            print(f"🔧 Сценарий {product_key} проанализирован: {scenario_result}")
            
            # Получаем данные клиента
            print(f"🔧 Получаем данные клиента для {product_key}...")
            try:
                client_data = scenario.get_client_data(client_code, days, db_manager)
                print(f"🔧 Данные клиента получены для {product_key}: {type(client_data)}")
            except Exception as e:
                print(f"❌ ОШИБКА получения данных клиента для {product_key}: {e}")
                raise
            
            # Генерируем уведомление
            print(f"🔧 Генерируем уведомление для {product_key}...")
            try:
                notification = integration.generate_notification_from_scenario(
                    client_data, scenario_result, scenario.product_name
                )
                print(f"🔧 Уведомление сгенерировано для {product_key}: {type(notification)}")
            except Exception as e:
                print(f"❌ ОШИБКА генерации уведомления для {product_key}: {e}")
                raise
            
            print(f"🔧 Обновляем уведомление для {product_key}...")
            try:
                notification.update({
                    'client_code': client_code,
                    'product_key': product_key,
                    'analysis_score': scenario_result.get('score', 0),
                    'expected_benefit': scenario_result.get('expected_benefit', 0)
                })
                print(f"🔧 Уведомление обновлено для {product_key}")
            except Exception as e:
                print(f"❌ ОШИБКА обновления уведомления для {product_key}: {e}")
                raise
            
            print(f"🔧 Добавляем уведомление в список для {product_key}...")
            try:
                notifications.append(notification)
                print(f"🔧 Уведомление добавлено в список для {product_key}")
            except Exception as e:
                print(f"❌ ОШИБКА добавления уведомления для {product_key}: {e}")
                raise
            
            print(f"✅ {product_key} завершен")
            
        except Exception as e:
            print(f"❌ ОШИБКА в {product_key}: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            # Продолжаем анализ других продуктов
            continue
    
    print(f"🔄 Цикл завершен: {len(notifications)} уведомлений")
    print(f"🔍 Список уведомлений: {[n.get('product_name', 'Unknown') for n in notifications]}")
    
    # Сортируем по приоритету и скорингу
    try:
        print(f"🔧 Начинаем сортировку...")
        notifications.sort(key=lambda x: (x.get('priority', 'low'), x.get('analysis_score', 0)), reverse=True)
        print(f"🔄 Сортировка: OK")
    except Exception as e:
        print(f"❌ ОШИБКА сортировки: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"🔧 После сортировки: {len(notifications)} уведомлений")

    print(f"🏆 Топ-3: {[n.get('product_name', 'Unknown') for n in notifications[:3]]}")
    
    # Убеждаемся, что возвращаем список, даже если он пустой
    if not notifications:
        print("⚠️ Нет уведомлений")
        return []
    
    print(f"✅ Анализ завершен: {len(notifications)} уведомлений за {time.time() - start_time:.1f}с")
    print(f"🔍 Возвращаем notifications: {type(notifications)}, длина: {len(notifications)}")
    return notifications
