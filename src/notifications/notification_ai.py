"""
Прокси-ИИ для генерации персонализированных уведомлений
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .message_templates import MessageTemplates


class NotificationAI:
    """Прокси-ИИ для генерации умных уведомлений"""
    
    def __init__(self):
        self.templates = MessageTemplates()
        self.rules = {
            'max_length': 220,  # Максимальная длина для пушей (180-220)
            'min_length': 50,   # Минимальная длина
            'max_emoji': 1,     # Максимум эмодзи (0-1 по смыслу)
            'max_exclamation': 1,  # Максимум восклицательных знаков (один максимум)
            'currency_format': '₸',  # Формат валюты (единый формат)
            'date_format': 'dd.mm.yyyy',  # Формат даты (дд.мм.гггг)
            'number_format': 'comma_space',  # Разряды — пробелы, дробная часть — запятая
            'no_caps': True,  # Без КАПС
            'action_verbs': ['открыть', 'настроить', 'посмотреть', 'оформить', 'узнать', 'попробовать', 'проверить', 'подключить', 'начать'],  # Глаголы действия
            'tone_requirements': {
                'personal_context': True,  # Персональный контекст (наблюдение по тратам/поведению)
                'benefit_explanation': True,  # Польза/объяснение (как продукт решает задачу)
                'friendly_tone': True,  # На равных, просто и по-человечески; доброжелательно
                'no_drama': True,  # Без драматизации и морали
                'important_first': True,  # Важное — в начало, без воды/канцеляризмов
                'light_humor': True,  # Допустим лёгкий, ненавязчивый юмор
                'no_pressure': True  # Никаких «крикливых» обещаний/давления
            }
        }
    
    def generate_notification(self, client_data: Dict, product_data: Dict, 
                            recommendation_data: Dict) -> Dict[str, Any]:
        """
        Генерация персонализированного уведомления
        
        Args:
            client_data: Данные клиента
            product_data: Данные продукта
            recommendation_data: Данные рекомендации
        
        Returns:
            Сгенерированное уведомление
        """
        # Извлекаем данные
        client_info = client_data.get('client_info', {})
        client_name = client_info.get('name', 'Клиент')
        client_status = client_info.get('status', 'active')
        
        # Определяем возрастную группу по статусу (так как age нет в схеме)
        age_group = self._get_age_group_by_status(client_status)
        
        # Получаем тон общения
        tone = self.templates.get_client_tone(age_group, client_status)
        
        # Определяем тип продукта
        product_name = product_data.get('name', '')
        product_type = self._map_product_to_type(product_name)
        
        # Генерируем сообщение
        message = self._generate_message(
            client_name, product_type, recommendation_data, 
            client_data, tone
        )
        
        # Валидируем и корректируем сообщение
        validated_message = self._validate_message(message, tone)
        
        return {
            'message': validated_message,
            'product_type': product_type,
            'client_name': client_name,
            'age_group': age_group,
            'tone': tone,
            'length': len(validated_message),
            'channels': self._get_recommended_channels(age_group, client_status),
            'priority': self._calculate_priority(recommendation_data),
            'personalization': self._get_personalization_level(recommendation_data)
        }
    
    def _get_age_group_by_status(self, status: str) -> str:
        """Определить возрастную группу по статусу клиента"""
        status_lower = status.lower()
        
        if 'студент' in status_lower:
            return 'young'
        elif 'зарплатный' in status_lower:
            return 'adult'
        elif 'премиальный' in status_lower:
            return 'middle'
        elif 'стандартный' in status_lower:
            return 'adult'
        else:
            return 'adult'  # По умолчанию
    
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
    
    def _generate_message(self, client_name: str, product_type: str, 
                         recommendation_data: Dict, client_data: Dict, 
                         tone: Dict) -> str:
        """Генерация сообщения на основе шаблона и данных"""
        
        # Получаем базовый шаблон
        template = self.templates.get_template(product_type, with_amount=True)
        
        # Подготавливаем данные для подстановки
        context = self._prepare_context(client_name, product_type, 
                                      recommendation_data, client_data)
        
        # Убеждаемся, что имя клиента есть в контексте
        context['name'] = client_name
        
        # Применяем тон общения
        template = self._apply_tone(template, tone)
        
        # Заполняем шаблон
        try:
            message = template.format(**context)
        except KeyError as e:
            # Если не хватает данных, используем базовый шаблон
            template = self.templates.get_template(product_type, with_amount=False)
            context = self._prepare_basic_context(client_name, product_type)
            message = template.format(**context)
        
        # Убираем лишние символы валюты
        message = message.replace('₸ ₸', '₸')
        
        return message
    
    def _prepare_context(self, client_name: str, product_type: str, 
                        recommendation_data: Dict, client_data: Dict) -> Dict[str, Any]:
        """Подготовка контекста для подстановки в шаблон"""
        context = {
            'name': client_name,
            'month': self.templates.format_date(datetime.now())
        }
        
        # Добавляем данные о тратах/балансе
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Специфичные данные для разных продуктов
        if product_type == 'travel_card':
            # Данные о тратах на путешествия
            if hasattr(self, 'travel_data') and self.travel_data:
                context['amount'] = self.templates.format_amount(self.travel_data['travel_amount'])
                context['cashback'] = self.templates.format_amount(self.travel_data['potential_cashback'])
            else:
                context['amount'] = self.templates.format_amount(50000)  # Примерная сумма
                context['cashback'] = self.templates.format_amount(2000)  # 4% кешбэк
        
        elif product_type == 'premium_card':
            context['balance'] = self.templates.format_amount(avg_balance)
            context['cashback'] = self.templates.format_amount(avg_balance * 0.02)  # 2% кешбэк
        
        elif product_type == 'credit_card':
            # Топ категории трат
            context['cat1'] = 'онлайн-покупки'
            context['cat2'] = 'доставка'
            context['cat3'] = 'развлечения'
            context['amount'] = self.templates.format_amount(30000)
            context['cashback'] = self.templates.format_amount(3000)
        
        elif product_type in ['multi_currency_deposit', 'savings_deposit', 'accumulation_deposit']:
            context['amount'] = self.templates.format_amount(avg_balance)
            interest_rate = 0.145 if 'мультивалютный' in product_type else 0.165
            context['profit'] = self.templates.format_amount(avg_balance * interest_rate)
        
        elif product_type == 'currency_exchange':
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
    
    def _apply_tone(self, template: str, tone: Dict) -> str:
        """Применение тона общения к шаблону"""
        # Корректируем формальность
        if tone['formality'] == 'casual':
            template = template.replace('Добрый день', 'Привет')
        elif tone['formality'] == 'very_formal':
            template = template.replace('Добрый день', 'Уважаемый')
        
        # Добавляем эмодзи если нужно
        if tone['emoji_usage'] == 'moderate' and '₸' in template:
            template = template.replace('₸', '₸ ✨')
        
        # Убираем лишние пробелы
        template = template.replace('  ', ' ')
        
        return template
    
    def _validate_message(self, message: str, tone: Dict) -> str:
        """Валидация и корректировка сообщения согласно TOV"""
        # Проверяем длину (180-220 символов для пушей)
        if len(message) > self.rules['max_length']:
            message = message[:self.rules['max_length'] - 3] + '...'
        elif len(message) < 50:
            message = message + ' Узнать подробнее?'
        
        # Убираем лишние восклицательные знаки (максимум 1)
        exclamation_count = message.count('!')
        if exclamation_count > self.rules['max_exclamation']:
            # Оставляем только первый восклицательный знак
            message = message.replace('!', '', exclamation_count - 1)
        
        # Убираем КАПС (строго запрещено)
        if message.isupper():
            message = message.capitalize()
        
        # Убираем лишние пробелы
        message = ' '.join(message.split())
        
        # Исправляем дублирование символа валюты
        message = message.replace('₸ ₸', '₸')
        message = message.replace('₸₸', '₸')
        
        # Правильное форматирование валюты (пробел перед ₸)
        # Сначала убираем все пробелы вокруг ₸
        message = message.replace(' ₸', '₸').replace('₸ ', '₸')
        # Затем добавляем пробел только перед ₸
        message = message.replace('₸', ' ₸')
        # Убираем двойные пробелы
        message = message.replace('  ₸', ' ₸')
        
        return message
    
    def _get_recommended_channels(self, age_group: str, status: str) -> List[str]:
        """Рекомендуемые каналы для отправки"""
        channels = ['push']
        
        if age_group in ['young', 'adult']:
            channels.append('sms')
        
        if status == 'premium':
            channels.append('email')
        
        return channels
    
    def _calculate_priority(self, recommendation_data: Dict) -> str:
        """Расчет приоритета уведомления"""
        score = recommendation_data.get('match_score', {}).get('score', 0)
        
        if score > 0.8:
            return 'high'
        elif score > 0.5:
            return 'medium'
        else:
            return 'low'
    
    def _get_personalization_level(self, recommendation_data: Dict) -> str:
        """Уровень персонализации"""
        reasons = recommendation_data.get('match_score', {}).get('reasons', [])
        
        if len(reasons) >= 3:
            return 'high'
        elif len(reasons) >= 2:
            return 'medium'
        else:
            return 'low'
