"""
Пайплайн для обработки уведомлений
"""

from typing import Dict, List, Any, Optional
from .scenario_integration import ScenarioIntegration
from .notification_ai import NotificationAI
from .message_templates import MessageTemplates


class NotificationPipeline:
    """Основной пайплайн для обработки уведомлений"""
    
    def __init__(self):
        self.scenario_integration = ScenarioIntegration()
        self.ai = NotificationAI()
        self.templates = MessageTemplates()
    
    def process_client_analysis(self, client_data: Dict, 
                              scenario_results: List[Dict]) -> List[Dict[str, Any]]:
        """
        Обработка анализа клиента и генерация уведомлений
        
        Args:
            client_data: Данные клиента
            scenario_results: Результаты анализа по сценариям
        
        Returns:
            Список сгенерированных уведомлений
        """
        notifications = []
        
        for scenario_result in scenario_results:
            try:
                # Генерируем уведомление на основе сценария
                notification = self.scenario_integration.generate_notification_from_scenario(
                    client_data, 
                    scenario_result, 
                    scenario_result.get('product_name', 'Неизвестный продукт')
                )
                
                # Добавляем дополнительные данные
                notification.update({
                    'client_code': client_data.get('client_code'),
                    'analysis_score': scenario_result.get('score', 0),
                    'expected_benefit': scenario_result.get('expected_benefit', 0),
                    'product_key': scenario_result.get('product_key', 'unknown')
                })
                
                notifications.append(notification)
                
            except Exception as e:
                print(f"Ошибка генерации уведомления: {e}")
                continue
        
        # Сортируем по приоритету и скорингу
        notifications.sort(key=lambda x: (x.get('priority', 'low'), x.get('analysis_score', 0)), reverse=True)
        
        return notifications
    
    def generate_single_notification(self, client_data: Dict, 
                                   product_name: str, 
                                   scenario_result: Dict) -> Dict[str, Any]:
        """
        Генерация одного уведомления
        
        Args:
            client_data: Данные клиента
            product_name: Название продукта
            scenario_result: Результат анализа сценария
        
        Returns:
            Сгенерированное уведомление
        """
        return self.scenario_integration.generate_notification_from_scenario(
            client_data, scenario_result, product_name
        )
    
    def validate_notification(self, notification: Dict[str, Any]) -> bool:
        """
        Валидация уведомления
        
        Args:
            notification: Уведомление для валидации
        
        Returns:
            True если уведомление валидно
        """
        required_fields = ['message', 'product_name', 'client_name']
        
        for field in required_fields:
            if field not in notification or not notification[field]:
                return False
        
        # Проверяем длину сообщения
        message = notification.get('message', '')
        if len(message) < 10 or len(message) > 500:
            return False
        
        return True
    
    def get_recommended_channels(self, client_data: Dict) -> List[str]:
        """
        Получение рекомендуемых каналов для отправки
        
        Args:
            client_data: Данные клиента
        
        Returns:
            Список рекомендуемых каналов
        """
        return self.scenario_integration._get_recommended_channels(
            client_data.get('client_info', {})
        )
