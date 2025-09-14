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
    
    print(f"📊 Анализируем {len(scenarios)} продуктов...")
    
    for product_key, scenario in scenarios.items():
        try:
            # Проверяем таймаут (максимум 15 секунд)
            if time.time() - start_time > 15:
                print(f"⏰ Таймаут, завершаем с {len(notifications)} продуктами")
                break
                
            # Анализируем клиента
            scenario_result = scenario.analyze_client(client_code, days, db_manager)
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
            print(f"❌ {product_key}: {e}")
            # Продолжаем анализ других продуктов
            continue
    
    print(f"🔄 Обработано: {len(notifications)} продуктов")
    
    # Сортируем по приоритету и скорингу
    try:
        notifications.sort(key=lambda x: (x.get('priority', 'low'), x.get('analysis_score', 0)), reverse=True)
    except Exception as e:
        print(f"❌ Ошибка сортировки: {e}")
    
    print(f"🏆 Топ-3: {[n.get('product_name', 'Unknown') for n in notifications[:3]]}")
    
    if not notifications:
        return []
    
    print(f"✅ Завершено за {time.time() - start_time:.1f}с")
    return notifications


def analyze_client_fast(client_code: str, days: int, db_manager) -> List[Dict[str, Any]]:
    """Быстрый анализ клиента - только топ-5 продуктов"""
    from ..notifications.scenario_integration import ScenarioIntegration
    
    print(f"🚀 Быстрый анализ клиента {client_code}")
    
    try:
        integration = ScenarioIntegration()
        notifications = []
        
        # Анализируем только самые популярные продукты
        scenarios = {
            'travel_card': TravelCardScenario(),
            'credit_card': CreditCardScenario(),
            'investments': InvestmentsScenario(),
            'premium_card': PremiumCardScenario(),
            'cash_credit': CashCreditScenario()
        }
        
        for product_key, scenario in scenarios.items():
            try:
                print(f"🔍 {product_key}...", end=" ")
                
                # Анализируем клиента
                scenario_result = scenario.analyze_client(client_code, days, db_manager)
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
                print(f"✅")
                
            except Exception as e:
                print(f"❌ {e}")
                continue
        
        # Сортируем по скорингу
        notifications.sort(key=lambda x: x.get('analysis_score', 0), reverse=True)
        
        print(f"🚀 Быстрый анализ завершен: {len(notifications)} уведомлений")
        return notifications
        
    except Exception as e:
        print(f"❌ Ошибка быстрого анализа: {e}")
        return []
