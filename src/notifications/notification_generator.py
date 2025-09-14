"""
Генератор уведомлений для рекомендаций
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .notification_ai import NotificationAI
from .message_templates import MessageTemplates


class NotificationGenerator:
    """Генератор уведомлений на основе рекомендаций"""
    
    def __init__(self):
        self.ai = NotificationAI()
        self.templates = MessageTemplates()
    
    def generate_recommendation_notifications(self, recommendations: Dict) -> List[Dict[str, Any]]:
        """
        Генерация уведомлений для всех рекомендаций
        
        Args:
            recommendations: Результат работы RecommendationEngine
        
        Returns:
            Список уведомлений
        """
        notifications = []
        
        client_code = recommendations.get('client_code')
        client_info = recommendations.get('client_info', {})
        recommendation_list = recommendations.get('recommendations', [])
        
        # Подготавливаем данные клиента
        client_data = {
            'client_info': client_info,
            'transactions': [],  # Будет заполнено при необходимости
            'transfers': []
        }
        
        # Генерируем уведомления для каждой рекомендации
        for i, rec in enumerate(recommendation_list):
            product = rec.get('product', {})
            match_score = rec.get('match_score', {})
            
            # Генерируем уведомление
            notification = self.ai.generate_notification(
                client_data, product, match_score
            )
            
            # Добавляем метаданные
            notification.update({
                'client_code': client_code,
                'product_id': product.get('id'),
                'product_name': product.get('name'),
                'recommendation_rank': i + 1,
                'score': match_score.get('score', 0),
                'expected_benefit': rec.get('expected_benefit', 0),
                'generated_at': datetime.now().isoformat(),
                'template_used': self._get_template_used(product.get('name'))
            })
            
            notifications.append(notification)
        
        # Сортируем по приоритету и скорингу
        notifications.sort(key=lambda x: (x['priority'], x['score']), reverse=True)
        
        return notifications
    
    def generate_travel_card_notification(self, client_data: Dict, 
                                        travel_data: Dict) -> Dict[str, Any]:
        """
        Специальное уведомление для карты путешествий с детальными данными
        
        Args:
            client_data: Данные клиента
            travel_data: Данные о тратах на путешествия
        
        Returns:
            Уведомление для карты путешествий
        """
        client_info = client_data.get('client_info', {})
        client_name = client_info.get('name', 'Клиент')
        
        # Формируем персонализированное сообщение
        travel_amount = travel_data.get('travel_amount', 0)
        potential_cashback = travel_data.get('potential_cashback', 0)
        
        # Определяем категории трат
        categories = []
        if travel_data.get('travel_transactions'):
            for trans in travel_data['travel_transactions'][:3]:  # Топ-3
                category = trans.get('category', '')
                if category and category not in categories:
                    categories.append(category)
        
        # Формируем сообщение
        if categories:
            category_text = ', '.join(categories[:2])  # Максимум 2 категории
            message = f"{client_name}, в этом месяце вы активно тратите на {category_text}. "
        else:
            message = f"{client_name}, в этом месяце у вас много поездок. "
        
        message += f"С тревел-картой получили бы {self.templates.format_amount(potential_cashback)} кешбэка. Оформить карту?"
        
        # Валидируем длину
        if len(message) > 220:
            message = f"{client_name}, с тревел-картой получили бы {self.templates.format_amount(potential_cashback)} кешбэка. Оформить карту?"
        
        return {
            'message': message,
            'product_type': 'travel_card',
            'client_name': client_name,
            'travel_amount': travel_amount,
            'potential_cashback': potential_cashback,
            'categories': categories,
            'length': len(message),
            'priority': 'high' if potential_cashback > 5000 else 'medium',
            'channels': ['push', 'sms'],
            'personalization': 'high'
        }
    
    def generate_premium_card_notification(self, client_data: Dict, 
                                         balance: float) -> Dict[str, Any]:
        """Специальное уведомление для премиальной карты"""
        client_info = client_data.get('client_info', {})
        client_name = client_info.get('name', 'Клиент')
        
        # Рассчитываем потенциальный кешбэк
        monthly_cashback = balance * 0.02  # 2% базовый кешбэк
        if balance > 6000000:  # 6 млн
            monthly_cashback = balance * 0.04  # 4% премиальный кешбэк
        
        message = f"{client_name}, с остатком {self.templates.format_amount(balance)} премиальная карта даст до {self.templates.format_amount(monthly_cashback)} кешбэка в месяц. Оформить карту?"
        
        return {
            'message': message,
            'product_type': 'premium_card',
            'client_name': client_name,
            'balance': balance,
            'potential_cashback': monthly_cashback,
            'length': len(message),
            'priority': 'high' if balance > 3000000 else 'medium',
            'channels': ['push', 'email'],
            'personalization': 'high'
        }
    
    def generate_currency_notification(self, client_data: Dict, 
                                     currency_operations: int) -> Dict[str, Any]:
        """Специальное уведомление для валютных операций"""
        client_info = client_data.get('client_info', {})
        client_name = client_info.get('name', 'Клиент')
        
        if currency_operations > 5:
            message = f"{client_name}, вы часто меняете валюту. В приложении выгодный курс и авто-покупка по целевому курсу. Настроить обмен?"
        else:
            message = f"{client_name}, для удобства валютных операций настройте обмен в приложении. Выгодный курс без комиссии. Настроить?"
        
        return {
            'message': message,
            'product_type': 'currency_exchange',
            'client_name': client_name,
            'currency_operations': currency_operations,
            'length': len(message),
            'priority': 'medium',
            'channels': ['push'],
            'personalization': 'medium'
        }
    
    def _get_template_used(self, product_name: str) -> str:
        """Получить использованный шаблон"""
        mapping = {
            'Карта для путешествий': 'travel_card_template',
            'Премиальная карта': 'premium_card_template',
            'Кредитная карта': 'credit_card_template',
            'Обмен валют': 'currency_exchange_template',
            'Депозит Мультивалютный': 'deposit_template',
            'Депозит Сберегательный': 'deposit_template',
            'Депозит Накопительный': 'deposit_template',
            'Инвестиции': 'investments_template',
            'Золотые слитки': 'gold_template',
            'Кредит наличными': 'credit_template'
        }
        return mapping.get(product_name, 'generic_template')
    
    def validate_notification(self, notification: Dict) -> Dict[str, Any]:
        """Валидация уведомления"""
        issues = []
        
        message = notification.get('message', '')
        
        # Проверяем длину
        if len(message) > 220:
            issues.append('Сообщение слишком длинное')
        elif len(message) < 50:
            issues.append('Сообщение слишком короткое')
        
        # Проверяем наличие имени клиента
        if 'name' not in message.lower() and 'клиент' not in message.lower():
            issues.append('Отсутствует персонализация')
        
        # Проверяем наличие призыва к действию
        action_words = ['оформить', 'открыть', 'настроить', 'узнать', 'посмотреть']
        if not any(word in message.lower() for word in action_words):
            issues.append('Отсутствует призыв к действию')
        
        # Проверяем форматирование валюты
        if '₸' in message and ' ' not in message.split('₸')[0][-2:]:
            issues.append('Некорректное форматирование валюты')
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'score': max(0, 100 - len(issues) * 20)  # Оценка от 0 до 100
        }
