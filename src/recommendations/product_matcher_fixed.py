"""
Сопоставитель продуктов с клиентами (исправленная версия под реальную БД)
"""

from typing import Dict, List, Any, Optional
from ..products.cash_credit import CashCreditScenario
from ..products.credit_card import CreditCardScenario
from ..products.premium_card import PremiumCardScenario
from ..products.travel_card_fixed import TravelCardScenario
from ..products.savings_deposit import SavingsDepositScenario
from ..products.accumulation_deposit import AccumulationDepositScenario
from ..products.multi_currency_deposit import MultiCurrencyDepositScenario
from ..products.gold_bars import GoldBarsScenario
from ..products.investments import InvestmentsScenario
from ..products.currency_exchange import CurrencyExchangeScenario


class ProductMatcher:
    """Класс для сопоставления продуктов с клиентами"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        
        # Инициализируем все сценарии продуктов
        self.cash_credit_scenario = CashCreditScenario()
        self.credit_card_scenario = CreditCardScenario()
        self.premium_card_scenario = PremiumCardScenario()
        self.travel_card_scenario = TravelCardScenario()
        self.savings_deposit_scenario = SavingsDepositScenario()
        self.accumulation_deposit_scenario = AccumulationDepositScenario()
        self.multi_currency_deposit_scenario = MultiCurrencyDepositScenario()
        self.gold_bars_scenario = GoldBarsScenario()
        self.investments_scenario = InvestmentsScenario()
        self.currency_exchange_scenario = CurrencyExchangeScenario()
    
    def get_available_scenarios(self) -> Dict[str, Any]:
        """Получить список всех доступных сценариев продуктов"""
        return {
            'cash_credit': self.cash_credit_scenario,
            'credit_card': self.credit_card_scenario,
            'premium_card': self.premium_card_scenario,
            'travel_card': self.travel_card_scenario,
            'savings_deposit': self.savings_deposit_scenario,
            'accumulation_deposit': self.accumulation_deposit_scenario,
            'multi_currency_deposit': self.multi_currency_deposit_scenario,
            'gold_bars': self.gold_bars_scenario,
            'investments': self.investments_scenario,
            'currency_exchange': self.currency_exchange_scenario
        }
    
    def match_client_to_products(self, client_code: str, products: List[Dict]) -> List[Dict]:
        """
        Сопоставить клиента с продуктами
        
        Args:
            client_code: Код клиента
            products: Список продуктов
        
        Returns:
            Список продуктов с оценками соответствия
        """
        matched_products = []
        
        for product in products:
            match_result = self._analyze_product_match(client_code, product)
            if match_result['is_match']:
                matched_products.append({
                    'product': product,
                    'match_result': match_result
                })
        
        return matched_products
    
    def _analyze_product_match(self, client_code: str, product: Dict) -> Dict[str, Any]:
        """
        Анализ соответствия клиента продукту
        
        Args:
            client_code: Код клиента
            product: Данные продукта
        
        Returns:
            Результат анализа соответствия
        """
        # Базовый анализ соответствия
        match_result = {
            'is_match': False,
            'score': 0.0,
            'reasons': [],
            'expected_benefit': 0.0
        }
        
        # Получаем информацию о клиенте
        client_info = self.db.get_client_by_code(client_code)
        if not client_info:
            return match_result
        
        # Анализируем по категории продукта и названию
        product_category = product.get('category', '')
        product_name = product.get('name', '').lower()
        
        # Используем специализированные сценарии для конкретных продуктов
        if 'кредит наличными' in product_name or (product_category == 'loans' and 'наличными' in product_name):
            match_result = self.cash_credit_scenario.analyze_client(client_code, 90, self.db)
        elif 'кредитная карта' in product_name or (product_category == 'cards' and 'кредитная' in product_name):
            match_result = self.credit_card_scenario.analyze_client(client_code, 90, self.db)
        elif 'премиальная карта' in product_name or (product_category == 'cards' and 'премиальная' in product_name):
            match_result = self.premium_card_scenario.analyze_client(client_code, 90, self.db)
        elif 'карта для путешествий' in product_name or (product_category == 'cards' and 'путешествий' in product_name):
            match_result = self.travel_card_scenario.analyze_client(client_code, 90, self.db)
        elif 'сберегательный депозит' in product_name or (product_category == 'deposits' and 'сберегательный' in product_name):
            match_result = self.savings_deposit_scenario.analyze_client(client_code, 90, self.db)
        elif 'накопительный депозит' in product_name or (product_category == 'deposits' and 'накопительный' in product_name):
            match_result = self.accumulation_deposit_scenario.analyze_client(client_code, 90, self.db)
        elif 'мультивалютный депозит' in product_name or (product_category == 'deposits' and 'мультивалютный' in product_name):
            match_result = self.multi_currency_deposit_scenario.analyze_client(client_code, 90, self.db)
        elif 'золотые слитки' in product_name or (product_category == 'investments' and 'золотые' in product_name):
            match_result = self.gold_bars_scenario.analyze_client(client_code, 90, self.db)
        elif 'инвестиции' in product_name or product_category == 'investments':
            match_result = self.investments_scenario.analyze_client(client_code, 90, self.db)
        elif 'валютный обмен' in product_name or product_category == 'currency':
            match_result = self.currency_exchange_scenario.analyze_client(client_code, 90, self.db)
        # Fallback на базовые методы для неизвестных продуктов
        elif product_category == 'cards':
            match_result = self._analyze_card_match(client_info, product)
        elif product_category == 'deposits':
            match_result = self._analyze_deposit_match(client_info, product)
        elif product_category == 'credits' or product_category == 'loans':
            match_result = self._analyze_credit_match(client_info, product)
        elif product_category == 'investments':
            match_result = self._analyze_investment_match(client_info, product)
        else:
            match_result = self._analyze_generic_match(client_info, product)
        
        return match_result
    
    # Базовые методы анализа остаются как fallback для неизвестных продуктов
    # или когда специализированные сценарии недоступны
    
    def _analyze_card_match(self, client_info: Dict, product: Dict) -> Dict[str, Any]:
        """Анализ соответствия карточным продуктам"""
        match_result = {
            'is_match': False,
            'score': 0.0,
            'reasons': [],
            'expected_benefit': 0.0
        }
        
        avg_balance = float(client_info.get('avg_monthly_balance_kzt', 0))
        product_name = product.get('name', '')
        status = client_info.get('status', '')
        age = client_info.get('age', 0)
        
        # Базовые правила для карт
        if avg_balance > 1000000:  # 1 млн тенге
            match_result['score'] += 0.3
            match_result['reasons'].append('Высокий средний баланс')
        
        if avg_balance > 6000000:  # 6 млн тенге
            match_result['score'] += 0.5
            match_result['reasons'].append('Очень высокий баланс - подходит для премиальных карт')
        
        # Анализ по статусу клиента
        if status == 'Премиальный клиент':
            match_result['score'] += 0.4
            match_result['reasons'].append('Премиальный статус клиента')
        elif status == 'Зарплатный клиент':
            match_result['score'] += 0.3
            match_result['reasons'].append('Зарплатный клиент - стабильный доход')
        elif status == 'Студент':
            match_result['score'] += 0.1
            match_result['reasons'].append('Студент - ограниченные возможности')
        
        # Анализ по возрасту
        if 20 <= age <= 39:  # Основная ЦА
            match_result['score'] += 0.2
            match_result['reasons'].append('Входит в основную целевую аудиторию')
        
        # Специфичные правила для разных карт
        if 'путешествий' in product_name.lower():
            # Анализ трат на путешествия будет добавлен позже
            match_result['score'] += 0.2
            match_result['reasons'].append('Потенциально подходит для путешествий')
        
        if 'премиальная' in product_name.lower():
            if avg_balance > 3000000:  # 3 млн тенге
                match_result['score'] += 0.4
                match_result['reasons'].append('Подходит для премиальной карты')
        
        if 'кредитная' in product_name.lower():
            match_result['score'] += 0.2
            match_result['reasons'].append('Кредитная карта доступна всем')
        
        # Определяем соответствие
        if match_result['score'] > 0.3:
            match_result['is_match'] = True
            match_result['expected_benefit'] = avg_balance * 0.02  # 2% от баланса
        
        return match_result
    
    def _analyze_deposit_match(self, client_info: Dict, product: Dict) -> Dict[str, Any]:
        """Анализ соответствия депозитным продуктам"""
        match_result = {
            'is_match': False,
            'score': 0.0,
            'reasons': [],
            'expected_benefit': 0.0
        }
        
        avg_balance = float(client_info.get('avg_monthly_balance_kzt', 0))
        product_name = product.get('name', '')
        status = client_info.get('status', '')
        
        # Базовые правила для депозитов
        if avg_balance > 500000:  # 500 тыс тенге
            match_result['score'] += 0.4
            match_result['reasons'].append('Есть свободные средства для депозита')
        
        if avg_balance > 2000000:  # 2 млн тенге
            match_result['score'] += 0.3
            match_result['reasons'].append('Большой баланс - подходит для крупных депозитов')
        
        # Анализ по статусу
        if status == 'Премиальный клиент':
            match_result['score'] += 0.3
            match_result['reasons'].append('Премиальный клиент - приоритет для депозитов')
        elif status == 'Зарплатный клиент':
            match_result['score'] += 0.2
            match_result['reasons'].append('Зарплатный клиент - регулярные поступления')
        
        # Специфичные правила для разных депозитов
        if 'мультивалютный' in product_name.lower():
            match_result['score'] += 0.2
            match_result['reasons'].append('Мультивалютный депозит для диверсификации')
        
        if 'сберегательный' in product_name.lower():
            if avg_balance > 1000000:  # 1 млн тенге
                match_result['score'] += 0.3
                match_result['reasons'].append('Подходит для сберегательного депозита')
        
        if 'накопительный' in product_name.lower():
            match_result['score'] += 0.2
            match_result['reasons'].append('Накопительный депозит для регулярных сбережений')
        
        # Определяем соответствие
        if match_result['score'] > 0.4:
            match_result['is_match'] = True
            # Ожидаемая выгода зависит от ставки депозита
            interest_rate = product.get('interest_rate', 0.15)  # 15% по умолчанию
            match_result['expected_benefit'] = avg_balance * interest_rate
        
        return match_result
    
    def _analyze_credit_match(self, client_info: Dict, product: Dict) -> Dict[str, Any]:
        """Анализ соответствия кредитным продуктам"""
        match_result = {
            'is_match': False,
            'score': 0.0,
            'reasons': [],
            'expected_benefit': 0.0
        }
        
        avg_balance = float(client_info.get('avg_monthly_balance_kzt', 0))
        product_name = product.get('name', '')
        status = client_info.get('status', '')
        
        # Базовые правила для кредитов
        if avg_balance > 200000:  # 200 тыс тенге
            match_result['score'] += 0.3
            match_result['reasons'].append('Стабильный доход для обслуживания кредита')
        
        # Анализ по статусу
        if status == 'Зарплатный клиент':
            match_result['score'] += 0.4
            match_result['reasons'].append('Зарплатный клиент - приоритет для кредитов')
        elif status == 'Премиальный клиент':
            match_result['score'] += 0.5
            match_result['reasons'].append('Премиальный клиент - лучшие условия кредитования')
        elif status == 'Студент':
            match_result['score'] += 0.1
            match_result['reasons'].append('Студент - ограниченные кредитные возможности')
        
        if 'наличными' in product_name.lower():
            match_result['score'] += 0.2
            match_result['reasons'].append('Кредит наличными доступен при наличии дохода')
        
        # Определяем соответствие
        if match_result['score'] > 0.3:
            match_result['is_match'] = True
            # Ожидаемая выгода - комиссия банка
            credit_limit = product.get('credit_limit', 1000000)  # 1 млн по умолчанию
            match_result['expected_benefit'] = credit_limit * 0.05  # 5% комиссия
        
        return match_result
    
    def _analyze_investment_match(self, client_info: Dict, product: Dict) -> Dict[str, Any]:
        """Анализ соответствия инвестиционным продуктам"""
        match_result = {
            'is_match': False,
            'score': 0.0,
            'reasons': [],
            'expected_benefit': 0.0
        }
        
        avg_balance = float(client_info.get('avg_monthly_balance_kzt', 0))
        product_name = product.get('name', '')
        status = client_info.get('status', '')
        age = client_info.get('age', 0)
        
        # Базовые правила для инвестиций
        if avg_balance > 1000000:  # 1 млн тенге
            match_result['score'] += 0.4
            match_result['reasons'].append('Достаточный капитал для инвестиций')
        
        # Анализ по статусу
        if status == 'Премиальный клиент':
            match_result['score'] += 0.3
            match_result['reasons'].append('Премиальный клиент - приоритет для инвестиций')
        elif status == 'Зарплатный клиент':
            match_result['score'] += 0.2
            match_result['reasons'].append('Зарплатный клиент - стабильный доход для инвестиций')
        
        # Анализ по возрасту
        if 25 <= age <= 45:  # Оптимальный возраст для инвестиций
            match_result['score'] += 0.2
            match_result['reasons'].append('Оптимальный возраст для инвестиций')
        
        if 'золотые' in product_name.lower():
            if avg_balance > 500000:  # 500 тыс тенге
                match_result['score'] += 0.3
                match_result['reasons'].append('Подходит для инвестиций в золото')
        
        # Определяем соответствие
        if match_result['score'] > 0.4:
            match_result['is_match'] = True
            # Ожидаемая выгода - потенциальный доход от инвестиций
            match_result['expected_benefit'] = avg_balance * 0.1  # 10% потенциальный доход
        
        return match_result
    
    def _analyze_generic_match(self, client_info: Dict, product: Dict) -> Dict[str, Any]:
        """Общий анализ соответствия"""
        match_result = {
            'is_match': True,  # По умолчанию подходит всем
            'score': 0.1,
            'reasons': ['Базовое соответствие'],
            'expected_benefit': 0.0
        }
        
        return match_result
