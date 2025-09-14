"""
Пример интеграции сценариев продуктов с генерацией уведомлений
"""

from typing import Dict, List, Any
from .scenario_integration import ScenarioIntegration
from ..products import (
    TravelCardScenario, PremiumCardScenario, CreditCardScenario,
    CurrencyExchangeScenario, MultiCurrencyDepositScenario,
    SavingsDepositScenario, AccumulationDepositScenario,
    InvestmentsScenario, GoldBarsScenario, CashCreditScenario
)


class NotificationPipeline:
    """Пайплайн для генерации уведомлений на основе анализа продуктов"""
    
    def __init__(self):
        self.integration = ScenarioIntegration()
        self.scenarios = {
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
    
    def analyze_and_generate_notifications(self, client_code: str, days: int, 
                                         db_manager) -> List[Dict[str, Any]]:
        """
        Анализ клиента и генерация уведомлений для всех продуктов
        
        Args:
            client_code: Код клиента
            days: Период анализа в днях
            db_manager: Менеджер базы данных
        
        Returns:
            Список уведомлений для всех продуктов
        """
        notifications = []
        
        # Анализируем клиента для каждого продукта
        for product_key, scenario in self.scenarios.items():
            try:
                # Получаем результат анализа сценария
                scenario_result = scenario.analyze_client(client_code, days, db_manager)
                
                # Получаем данные клиента
                client_data = scenario.get_client_data(client_code, days, db_manager)
                
                # Генерируем уведомление
                notification = self.integration.generate_notification_from_scenario(
                    client_data, scenario_result, scenario.product_name
                )
                
                # Добавляем метаданные
                notification.update({
                    'client_code': client_code,
                    'product_key': product_key,
                    'analysis_score': scenario_result.get('score', 0),
                    'expected_benefit': scenario_result.get('expected_benefit', 0)
                })
                
                notifications.append(notification)
                
            except Exception as e:
                print(f"Ошибка анализа продукта {product_key} для клиента {client_code}: {e}")
                continue
        
        # Сортируем по приоритету и скорингу
        notifications.sort(key=lambda x: (x['priority'], x['analysis_score']), reverse=True)
        
        return notifications
    
    def get_best_recommendation(self, notifications: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Получить лучшую рекомендацию (топ-1)"""
        if not notifications:
            return {}
        
        return notifications[0]
    
    def get_top_recommendations(self, notifications: List[Dict[str, Any]], 
                              top_n: int = 4) -> List[Dict[str, Any]]:
        """Получить топ-N рекомендаций"""
        return notifications[:top_n]
    
    def generate_final_pushes_csv(self, notifications: List[Dict[str, Any]], 
                                filename: str = 'final_pushes.csv') -> str:
        """Генерация финального CSV файла с пуш-уведомлениями"""
        import csv
        
        # Фильтруем только уведомления с высоким и средним приоритетом
        filtered_notifications = [
            n for n in notifications 
            if n.get('priority') in ['high', 'medium']
        ]
        
        # Берем только топ-4
        top_notifications = filtered_notifications[:4]
        
        # Записываем в CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['client_code', 'product', 'push_notification', 'priority', 'score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for notification in top_notifications:
                writer.writerow({
                    'client_code': notification.get('client_code', ''),
                    'product': notification.get('product_name', ''),
                    'push_notification': notification.get('message', ''),
                    'priority': notification.get('priority', ''),
                    'score': notification.get('analysis_score', 0)
                })
        
        return filename


def example_usage():
    """Пример использования пайплайна"""
    
    # Создаем пайплайн
    pipeline = NotificationPipeline()
    
    # Пример данных клиента (в реальности получаем из БД)
    client_code = "12345"
    days = 90
    
    # Здесь должен быть реальный db_manager
    # db_manager = DatabaseManager()
    
    # Анализируем и генерируем уведомления
    # notifications = pipeline.analyze_and_generate_notifications(
    #     client_code, days, db_manager
    # )
    
    # Получаем лучшую рекомендацию
    # best_rec = pipeline.get_best_recommendation(notifications)
    # print(f"Лучшая рекомендация: {best_rec}")
    
    # Получаем топ-4 рекомендации
    # top_recs = pipeline.get_top_recommendations(notifications, 4)
    # print(f"Топ-4 рекомендации: {len(top_recs)}")
    
    # Генерируем CSV файл
    # csv_file = pipeline.generate_final_pushes_csv(notifications)
    # print(f"CSV файл создан: {csv_file}")


if __name__ == "__main__":
    example_usage()
