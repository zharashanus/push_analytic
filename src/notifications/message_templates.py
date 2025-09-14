"""
Шаблоны сообщений для уведомлений
"""

from typing import Dict, List, Any
from datetime import datetime


class MessageTemplates:
    """Шаблоны сообщений для разных продуктов"""
    
    def __init__(self):
        self.templates = {
            # 💳 Карты
            'travel_card': {
                'template': "{name}, в {month} у вас {trip_count} поездок на такси на {amount} ₸. С тревел-картой вернули бы {cashback} ₸ кешбэком. Хотите оформить?",
                'with_amount': "{name}, в {month} у вас {trip_count} поездок на такси на {amount} ₸. С тревел-картой вернули бы {cashback} ₸ кешбэком. Хотите оформить?",
                'categories': ['такси', 'отели', 'путешествия', 'транспорт']
            },
            'premium_card': {
                'template': "{name}, у вас стабильно крупный остаток {balance} ₸ и траты в ресторанах. Премиальная карта даст больше кешбэка и бесплатные снятия. Оформить карту.",
                'with_amount': "{name}, у вас стабильно крупный остаток {balance} ₸ и траты в ресторанах. Премиальная карта даст больше кешбэка и бесплатные снятия. Оформить карту.",
                'categories': ['рестораны', 'премиум', 'крупные траты']
            },
            'credit_card': {
                'template': "{name}, ваши топ-категории — {cat1}, {cat2}, {cat3}. Кредитная карта вернёт до {percent}% именно там. Оформить карту.",
                'with_amount': "{name}, в этом месяце на подписки ушло {amount} ₸. Карта с кешбэком вернула бы {cashback} ₸. Открыть карту.",
                'categories': ['онлайн', 'доставка', 'развлечения']
            },
            'multi_currency_card': {
                'template': "{name}, заметили ваши частые покупки в {fx_curr}. Мультивалютная карта поможет избежать конвертаций. Настроить карту.",
                'with_amount': "{name}, заметили ваши частые покупки в {fx_curr}. Мультивалютная карта поможет избежать конвертаций. Настроить карту.",
                'categories': ['валютные операции', 'обмен', 'usd', 'eur']
            },
            
            # 💰 Вклады и накопления
            'savings_deposit': {
                'template': "{name}, у вас свободно {balance} ₸ на карте. Разместите их на вкладе — удобно копить и получать доход. Открыть вклад.",
                'with_amount': "{name}, у вас свободно {balance} ₸ на карте. Разместите их на вкладе — удобно копить и получать доход. Открыть вклад.",
                'categories': ['сбережения', 'максимальный доход', 'защита']
            },
            'accumulation_deposit': {
                'template': "{name}, за последние {months} месяца у вас остаётся от {min_balance} ₸. На вкладе они работали бы на вас. Посмотреть варианты.",
                'with_amount': "{name}, деньги на карте {balance} ₸ не приносят дохода. На накопительном счёте они растут каждый месяц. Открыть счёт.",
                'categories': ['сбережения', 'накопления', 'регулярные взносы']
            },
            'multi_currency_deposit': {
                'template': "{name}, планируете отпуск в {month}? На вкладе можно накопить быстрее. Настроить вклад.",
                'with_amount': "{name}, храните {balance} ₸ на карте. На сберегательном счёте это даст вознаграждение уже через {period}. Попробовать.",
                'categories': ['сбережения', 'валюты', 'депозит']
            },
            
            # 📈 Инвестиции
            'investments': {
                'template': "{name}, попробуйте инвестиции с низким порогом — от {amount} ₸ и без комиссии на старт. Открыть счёт.",
                'with_amount': "{name}, вы накопили {balance} ₸. Инвестиции помогут сохранить и приумножить средства. Узнать подробнее.",
                'categories': ['инвестиции', 'низкий порог', 'без комиссий']
            },
            'investments_balance': {
                'template': "{name}, у вас часто остаются свободные {balance} ₸. Инвестиции — шанс их увеличить. Открыть счёт.",
                'with_amount': "{name}, в этом месяце у вас {balance} ₸ остаток. Запустите инвестиции — без сложностей и лишних рисков. Начать.",
                'categories': ['инвестиции', 'низкий порог', 'без комиссий']
            },
            'investments_simple': {
                'template': "{name}, хотите попробовать инвестиции без лишних терминов? В приложении это просто. Открыть счёт.",
                'with_amount': "{name}, хотите попробовать инвестиции без лишних терминов? В приложении это просто. Открыть счёт.",
                'categories': ['инвестиции', 'низкий порог', 'без комиссий']
            },
            
            # 🌍 Валюта и переводы
            'currency_exchange': {
                'template': "{name}, вы часто платите в {fx_curr}. В приложении выгодный обмен и авто-покупка по курсу {fx_rate}. Настроить обмен.",
                'with_amount': "{name}, в {month} вы потратили {amount} ₸ в {fx_curr}. С мультивалютным счётом можно избежать комиссий. Подключить.",
                'categories': ['валютные операции', 'обмен', 'usd', 'eur']
            },
            'currency_travel': {
                'template': "{name}, планируете поездку в {country}? В приложении обмен валюты по курсу {fx_rate}. Попробовать.",
                'with_amount': "{name}, у вас частые покупки в {fx_curr}. Настройте автообмен по курсу {fx_rate} — и не теряйте на конвертациях. Настроить.",
                'categories': ['валютные операции', 'обмен', 'usd', 'eur']
            },
            'multi_currency_account': {
                'template': "{name}, храните сбережения в {main_curr}? Можно держать часть в {fx_curr} — прямо в приложении. Открыть мультивалютный счёт.",
                'with_amount': "{name}, храните сбережения в {main_curr}? Можно держать часть в {fx_curr} — прямо в приложении. Открыть мультивалютный счёт.",
                'categories': ['сбережения', 'валюты', 'депозит']
            },
            
            # 🏦 Кредиты
            'cash_credit': {
                'template': "{name}, если нужен запас на крупные траты — можно оформить кредит наличными до {limit} ₸ с выплатами {terms}. Узнать лимит.",
                'with_amount': "{name}, собираетесь обновить {purchase_item}? Кредит наличными на {amount} ₸ поможет сразу. Узнать лимит.",
                'categories': ['кредит', 'наличные', 'гибкие выплаты']
            },
            'credit_card_installment': {
                'template': "{name}, у вас часто покупки в рассрочку. Кредитная карта даст {grace_period} дней без переплат. Оформить.",
                'with_amount': "{name}, у вас часто покупки в рассрочку. Кредитная карта даст {grace_period} дней без переплат. Оформить.",
                'categories': ['кредит', 'карта', 'рассрочка']
            },
            'personal_credit': {
                'template': "{name}, у вас стабильный доход {income} ₸. Доступен персональный кредит на выгодных условиях. Проверить предложение.",
                'with_amount': "{name}, не хватает средств на отпуск в {month}? Можно оформить кредит на {amount} ₸ и распределить выплаты. Посмотреть лимит.",
                'categories': ['кредит', 'персональный', 'выгодные условия']
            },
            
            # 🎯 Персональные ситуации
            'delivery_food': {
                'template': "{name}, в {month} траты на доставку еды выросли на {percent}%. С картой вернётся часть расходов. Открыть карту.",
                'with_amount': "{name}, в {month} траты на доставку еды выросли на {percent}%. С картой вернётся часть расходов. Открыть карту.",
                'categories': ['доставка', 'еда', 'кешбэк']
            },
            'subscriptions': {
                'template': "{name}, у вас {subscriptions_count} подписок: {sub1}, {sub2}, {sub3}. Кредитная карта вернёт до {percent}% на них. Попробовать.",
                'with_amount': "{name}, у вас {subscriptions_count} подписок: {sub1}, {sub2}, {sub3}. Кредитная карта вернёт до {percent}% на них. Попробовать.",
                'categories': ['подписки', 'онлайн', 'кешбэк']
            },
            'atm_withdrawals': {
                'template': "{name}, в {month} вы сняли {amount} ₸ в банкоматах. Премиальная карта делает это бесплатно. Узнать подробнее.",
                'with_amount': "{name}, в {month} вы сняли {amount} ₸ в банкоматах. Премиальная карта делает это бесплатно. Узнать подробнее.",
                'categories': ['банкоматы', 'снятие', 'премиум']
            },
            'taxi_carsharing': {
                'template': "{name}, на такси и каршеринг ушло {amount} ₸. С тревел-картой вернулись бы {cashback} ₸. Хотите оформить?",
                'with_amount': "{name}, на такси и каршеринг ушло {amount} ₸. С тревел-картой вернулись бы {cashback} ₸. Хотите оформить?",
                'categories': ['такси', 'каршеринг', 'транспорт']
            },
            'monthly_balance': {
                'template': "{name}, заметили, что у вас остаётся {balance} ₸ каждый месяц. На накопительном счёте это приносило бы {interest} ₸. Открыть.",
                'with_amount': "{name}, заметили, что у вас остаётся {balance} ₸ каждый месяц. На накопительном счёте это приносило бы {interest} ₸. Открыть.",
                'categories': ['сбережения', 'накопления', 'проценты']
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
        """Форматирование суммы в тенге согласно TOV (разряды — пробелы, дробная часть — запятая)"""
        if amount >= 1000000:
            return f"{amount/1000000:.1f} млн₸".replace('.', ',')
        elif amount >= 1000:
            # Форматируем с пробелами как разделителями разрядов
            formatted = f"{amount:,.0f}".replace(',', ' ')
            return f"{formatted}₸"
        else:
            return f"{amount:.0f}₸"
    
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
