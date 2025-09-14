"""
Интеграция сценариев продуктов с генерацией уведомлений
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .notification_ai import NotificationAI
from .message_templates import MessageTemplates


class ScenarioIntegration:
    """Интеграция данных из сценариев продуктов с уведомлениями"""
    
    def __init__(self):
        self.ai = NotificationAI()
        self.templates = MessageTemplates()
    
    def generate_notification_from_scenario(self, client_data: Dict, 
                                          scenario_result: Dict, 
                                          product_name: str) -> Dict[str, Any]:
        """
        Генерация уведомления на основе результата сценария продукта
        
        Args:
            client_data: Данные клиента
            scenario_result: Результат анализа сценария
            product_name: Название продукта
        
        Returns:
            Персонализированное уведомление
        """
        client_info = client_data.get('client_info', {})
        client_name = client_info.get('name', 'Клиент')
        
        # Извлекаем данные из сценария
        score = scenario_result.get('score', 0)
        reasons = scenario_result.get('reasons', [])
        expected_benefit = scenario_result.get('expected_benefit', 0)
        
        # Определяем тип продукта
        product_type = self._map_product_to_type(product_name)
        
        # Генерируем персонализированное сообщение
        message = self._generate_personalized_message(
            client_name, product_type, client_data, 
            scenario_result, expected_benefit
        )
        
        # Валидируем сообщение
        validated_message = self._validate_message(message)
        
        return {
            'message': validated_message,
            'product_type': product_type,
            'product_name': product_name,
            'client_name': client_name,
            'score': score,
            'expected_benefit': expected_benefit,
            'reasons': reasons,
            'length': len(validated_message),
            'priority': self._calculate_priority(score, expected_benefit),
            'channels': self._get_recommended_channels(client_info),
            'personalization': self._get_personalization_level(reasons)
        }
    
    def _map_product_to_type(self, product_name: str) -> str:
        """Маппинг названия продукта на тип"""
        mapping = {
            'Карта для путешествий': 'travel_card',
            'Премиальная карта': 'premium_card',
            'Кредитная карта': 'credit_card',
            'Обмен валют': 'currency_exchange',
            'Депозит Мультивалютный': 'multi_currency_deposit',
            'Депозит Сберегательный': 'savings_deposit',
            'Депозит Накопительный': 'accumulation_deposit',
            'Инвестиции': 'investments',
            'Золотые слитки': 'gold_bars',
            'Кредит наличными': 'cash_credit'
        }
        return mapping.get(product_name, 'generic')
    
    def _generate_personalized_message(self, client_name: str, product_type: str,
                                     client_data: Dict, scenario_result: Dict,
                                     expected_benefit: float) -> str:
        """Генерация персонализированного сообщения"""
        
        # Получаем базовый шаблон
        template = self.templates.get_template(product_type, with_amount=True)
        
        # Подготавливаем контекст
        context = self._prepare_context(client_name, product_type, client_data, 
                                      scenario_result, expected_benefit)
        
        # Заполняем шаблон
        try:
            message = template.format(**context)
        except KeyError as e:
            # Если не хватает данных, используем базовый шаблон
            template = self.templates.get_template(product_type, with_amount=False)
            context = self._prepare_basic_context(client_name, product_type)
            message = template.format(**context)
        
        return message
    
    def _prepare_context(self, client_name: str, product_type: str,
                        client_data: Dict, scenario_result: Dict,
                        expected_benefit: float) -> Dict[str, Any]:
        """Подготовка контекста для подстановки в шаблон"""
        context = {
            'name': client_name,
            'month': self.templates.format_date(datetime.now())
        }
        
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Специфичные данные для разных продуктов
        if product_type == 'travel_card':
            # Используем данные из travel_data если есть
            if hasattr(scenario_result, 'travel_data') and scenario_result.travel_data:
                travel_data = scenario_result.travel_data
                context['amount'] = self.templates.format_amount(travel_data.get('travel_amount', 0))
                context['cashback'] = self.templates.format_amount(travel_data.get('potential_cashback', 0))
            else:
                context['amount'] = self.templates.format_amount(50000)
                context['cashback'] = self.templates.format_amount(2000)
        
        elif product_type == 'premium_card':
            context['balance'] = self.templates.format_amount(avg_balance)
            context['cashback'] = self.templates.format_amount(avg_balance * 0.02)
        
        elif product_type == 'credit_card':
            # Используем данные из online_spending_data если есть
            if hasattr(scenario_result, 'online_spending_data') and scenario_result.online_spending_data:
                online_data = scenario_result.online_spending_data
                context['cat1'] = 'онлайн-покупки'
                context['cat2'] = 'доставка'
                context['cat3'] = 'развлечения'
                context['amount'] = self.templates.format_amount(online_data.get('online_amount', 0))
                context['cashback'] = self.templates.format_amount(online_data.get('potential_cashback', 0))
            else:
                context['cat1'] = 'онлайн-покупки'
                context['cat2'] = 'доставка'
                context['cat3'] = 'развлечения'
                context['amount'] = self.templates.format_amount(30000)
                context['cashback'] = self.templates.format_amount(3000)
        
        elif product_type in ['multi_currency_deposit', 'savings_deposit', 'accumulation_deposit']:
            context['amount'] = self.templates.format_amount(avg_balance)
            # Используем expected_benefit из сценария
            context['profit'] = self.templates.format_amount(expected_benefit)
        
        elif product_type == 'currency_exchange':
            # Используем данные из fx_data если есть
            if hasattr(scenario_result, 'fx_data') and scenario_result.fx_data:
                fx_data = scenario_result.fx_data
                context['fx_curr'] = 'USD'
                context['amount'] = self.templates.format_amount(fx_data.get('fx_amount', 0))
                context['savings'] = self.templates.format_amount(fx_data.get('potential_savings', 0))
            else:
                context['fx_curr'] = 'USD'
                context['amount'] = self.templates.format_amount(100000)
                context['savings'] = self.templates.format_amount(5000)
        
        elif product_type == 'investments':
            context['amount'] = self.templates.format_amount(10000)
        
        elif product_type == 'gold_bars':
            context['amount'] = self.templates.format_amount(500000)
        
        elif product_type == 'cash_credit':
            context['limit'] = self.templates.format_amount(2000000)
        
        return context
    
    def _prepare_basic_context(self, client_name: str, product_type: str) -> Dict[str, Any]:
        """Подготовка базового контекста без детальных данных"""
        return {
            'name': client_name,
            'month': self.templates.format_date(datetime.now()),
            'amount': '50 000 ₸',
            'cashback': '2 000 ₸',
            'balance': '1 000 000 ₸',
            'profit': '150 000 ₸'
        }
    
    def _validate_message(self, message: str) -> str:
        """Валидация сообщения согласно TOV"""
        # Проверяем длину (180-220 символов для пушей)
        if len(message) > 220:
            message = message[:217] + '...'
        elif len(message) < 50:
            message = message + ' Узнать подробнее?'
        
        # Убираем лишние восклицательные знаки (максимум 1)
        exclamation_count = message.count('!')
        if exclamation_count > 1:
            message = message.replace('!', '', exclamation_count - 1)
        
        # Убираем КАПС
        if message.isupper():
            message = message.capitalize()
        
        # Убираем лишние пробелы
        message = ' '.join(message.split())
        
        return message
    
    def _calculate_priority(self, score: float, expected_benefit: float) -> str:
        """Расчет приоритета уведомления"""
        if score > 0.8 and expected_benefit > 100000:
            return 'high'
        elif score > 0.5 and expected_benefit > 50000:
            return 'medium'
        else:
            return 'low'
    
    def _get_recommended_channels(self, client_info: Dict) -> List[str]:
        """Рекомендуемые каналы для отправки"""
        channels = ['push']
        status = client_info.get('status', '').lower()
        
        if 'премиальный' in status:
            channels.extend(['email', 'sms'])
        elif 'зарплатный' in status:
            channels.append('sms')
        
        return channels
    
    def _get_personalization_level(self, reasons: List[str]) -> str:
        """Уровень персонализации"""
        if len(reasons) >= 3:
            return 'high'
        elif len(reasons) >= 2:
            return 'medium'
        else:
            return 'low'
