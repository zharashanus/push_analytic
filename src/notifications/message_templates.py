"""
Шаблоны сообщений для уведомлений
"""

from typing import Dict, List, Any
from datetime import datetime


class MessageTemplates:
    """Шаблоны сообщений для разных продуктов"""
    
    def __init__(self):
        self.templates = {
            'travel_card': {
                'template': "{name}, в {month} у вас много поездок/такси. С тревел-картой часть расходов вернулась бы кешбэком. Хотите оформить?",
                'with_amount': "{name}, в {month} вы потратили {amount} ₸ на поездки. С тревел-картой получили бы {cashback} ₸ кешбэка. Оформить карту?",
                'categories': ['такси', 'отели', 'путешествия', 'транспорт']
            },
            'premium_card': {
                'template': "{name}, у вас стабильно крупный остаток и траты в ресторанах. Премиальная карта даст повышенный кешбэк и бесплатные снятия. Оформить сейчас.",
                'with_amount': "{name}, с остатком {balance} ₸ премиальная карта даст до {cashback} ₸ кешбэка в месяц. Оформить карту?",
                'categories': ['рестораны', 'премиум', 'крупные траты']
            },
            'credit_card': {
                'template': "{name}, ваши топ-категории — {cat1}, {cat2}, {cat3}. Кредитная карта даёт до 10% в любимых категориях и на онлайн-сервисы. Оформить карту.",
                'with_amount': "{name}, в {cat1} вы тратите {amount} ₸ в месяц. Кредитная карта вернёт {cashback} ₸ кешбэка. Оформить?",
                'categories': ['онлайн', 'доставка', 'развлечения']
            },
            'currency_exchange': {
                'template': "{name}, вы часто платите в {fx_curr}. В приложении выгодный обмен и авто-покупка по целевому курсу. Настроить обмен.",
                'with_amount': "{name}, в {month} вы обменяли {amount} ₸. С нашим курсом сэкономили бы {savings} ₸. Настроить обмен?",
                'categories': ['валютные операции', 'обмен', 'usd', 'eur']
            },
            'multi_currency_deposit': {
                'template': "{name}, у вас остаются свободные средства. Разместите их на мультивалютном вкладе — удобно копить и получать вознаграждение. Открыть вклад.",
                'with_amount': "{name}, с {amount} ₸ на мультивалютном вкладе получите {profit} ₸ в год. Открыть вклад?",
                'categories': ['сбережения', 'валюты', 'депозит']
            },
            'savings_deposit': {
                'template': "{name}, у вас остаются свободные средства. Разместите их на сберегательном вкладе — максимальный доход при защите KDIF. Открыть вклад.",
                'with_amount': "{name}, с {amount} ₸ на сберегательном вкладе получите {profit} ₸ в год. Открыть вклад?",
                'categories': ['сбережения', 'максимальный доход', 'защита']
            },
            'accumulation_deposit': {
                'template': "{name}, у вас остаются свободные средства. Разместите их на накопительном вкладе — удобно копить и получать вознаграждение. Открыть вклад.",
                'with_amount': "{name}, с {amount} ₸ на накопительном вкладе получите {profit} ₸ в год. Открыть вклад?",
                'categories': ['сбережения', 'накопления', 'регулярные взносы']
            },
            'investments': {
                'template': "{name}, попробуйте инвестиции с низким порогом входа и без комиссий на старт. Открыть счёт.",
                'with_amount': "{name}, с {amount} ₸ можно начать инвестировать. Без комиссий в первый год. Открыть счёт?",
                'categories': ['инвестиции', 'низкий порог', 'без комиссий']
            },
            'gold_bars': {
                'template': "{name}, для диверсификации портфеля рассмотрите золотые слитки 999,9 пробы. Хранение в сейфовых ячейках банка. Узнать подробнее.",
                'with_amount': "{name}, с {amount} ₸ можно купить золотые слитки для долгосрочного сохранения стоимости. Узнать подробнее?",
                'categories': ['золото', 'диверсификация', 'долгосрочные инвестиции']
            },
            'cash_credit': {
                'template': "{name}, если нужен запас на крупные траты — можно оформить кредит наличными с гибкими выплатами. Узнать доступный лимит.",
                'with_amount': "{name}, доступен кредит до {limit} ₸ наличными. Гибкие выплаты без штрафов. Узнать лимит?",
                'categories': ['кредит', 'наличные', 'гибкие выплаты']
            }
        }
    
    def get_template(self, product_type: str, with_amount: bool = False) -> str:
        """Получить шаблон сообщения"""
        if product_type not in self.templates:
            return "Доступен новый продукт. Узнать подробнее?"
        
        template_key = 'with_amount' if with_amount else 'template'
        return self.templates[product_type].get(template_key, self.templates[product_type]['template'])
    
    def get_categories(self, product_type: str) -> List[str]:
        """Получить категории для продукта"""
        return self.templates.get(product_type, {}).get('categories', [])
    
    def format_amount(self, amount: float) -> str:
        """Форматирование суммы в тенге"""
        if amount >= 1000000:
            return f"{amount/1000000:.1f} млн ₸"
        elif amount >= 1000:
            return f"{amount:,.0f} ₸".replace(',', ' ')
        else:
            return f"{amount:.0f} ₸"
    
    def format_date(self, date: datetime) -> str:
        """Форматирование даты"""
        months = [
            'январе', 'феврале', 'марте', 'апреле', 'мае', 'июне',
            'июле', 'августе', 'сентябре', 'октябре', 'ноябре', 'декабре'
        ]
        return months[date.month - 1]
    
    def get_age_group(self, birth_year: int) -> str:
        """Определить возрастную группу"""
        current_year = datetime.now().year
        age = current_year - birth_year
        
        if age < 25:
            return 'young'
        elif age < 35:
            return 'adult'
        elif age < 50:
            return 'middle'
        else:
            return 'senior'
    
    def get_client_tone(self, age_group: str, status: str) -> Dict[str, Any]:
        """Получить тон общения для клиента"""
        tones = {
            'young': {
                'formality': 'casual',
                'emoji_usage': 'moderate',
                'humor_level': 'high',
                'greeting': 'Привет'
            },
            'adult': {
                'formality': 'balanced',
                'emoji_usage': 'minimal',
                'humor_level': 'moderate',
                'greeting': 'Добрый день'
            },
            'middle': {
                'formality': 'formal',
                'emoji_usage': 'none',
                'humor_level': 'low',
                'greeting': 'Добрый день'
            },
            'senior': {
                'formality': 'very_formal',
                'emoji_usage': 'none',
                'humor_level': 'none',
                'greeting': 'Добрый день'
            }
        }
        
        base_tone = tones.get(age_group, tones['adult'])
        
        # Корректируем по статусу
        if status == 'premium':
            base_tone['formality'] = 'formal'
            base_tone['greeting'] = 'Уважаемый'
        
        return base_tone
