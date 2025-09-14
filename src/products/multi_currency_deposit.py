"""
Сценарий для мультивалютного депозита
Основан на авторитетных исследованиях валютного диверсификации и сберегательного поведения
"""

from typing import Dict, List, Any
from .base_scenario_fixed import BaseProductScenario


class MultiCurrencyDepositScenario(BaseProductScenario):
    """Сценарий для мультивалютного депозита"""
    
    def __init__(self):
        super().__init__()
        self.product_name = "Депозит Мультивалютный"
        self.category = "deposits"
        self.description = "14.50% ставка, KZT/USD/RUB/EUR, пополнение и снятие без ограничений"
        self.target_audience = "Клиенты для хранения/ребалансировки валют с доступом к деньгам"
        
        # Условия основаны на исследованиях валютного диверсификации
        self.conditions = {
            'min_balance': 1000000,  # 1 млн тенге (финансовая стабильность)
            'interest_rate': 0.145,  # 14.50% годовых
            'currencies': ['KZT', 'USD', 'RUB', 'EUR'],  # 4 валюты
            'min_currency_operations': 2,  # Минимум 2 валютные операции
            'min_balance_ratio': 0.1,  # 10% от баланса в валюте
            'flexibility': 'Пополнение и снятие без ограничений'
        }
        
        # Преимущества согласно требованиям
        self.benefits = {
            'interest_rate': 0.145,  # 14.50% годовых
            'currency_diversification': 4,  # 4 валюты для диверсификации
            'unlimited_access': True,  # Пополнение и снятие без ограничений
            'currency_rebalancing': True,  # Возможность ребалансировки
            'high_liquidity': True,  # Высокая ликвидность
            'risk_mitigation': True  # Снижение валютных рисков
        }
    
    def analyze_client(self, client_code: str, days: int, db_manager) -> Dict[str, Any]:
        """
        Анализ соответствия клиента мультивалютному депозиту
        Основан на исследованиях валютного диверсификации и сберегательного поведения
        """
        client_data = self.get_client_data(client_code, days, db_manager)
        if not client_data:
            return self.format_analysis_result(0, ['Клиент не найден'], 0)
        
        reasons = []
        score = 0.0
        
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        status = client_info.get('status', '')
        
        # 1. Анализ финансовой стабильности (основной критерий - 40%)
        stability_score = self._analyze_financial_stability(avg_balance, status)
        score += stability_score * 0.4
        if stability_score > 0.8:
            reasons.append('Высокая финансовая стабильность для мультивалютного депозита')
        elif stability_score > 0.5:
            reasons.append('Достаточная финансовая стабильность')
        
        # 2. Анализ валютной активности (ключевой фактор - 35%)
        currency_score = self._analyze_currency_activity(client_data)
        score += currency_score * 0.35
        if currency_score > 0.7:
            reasons.append('Активные валютные операции - идеально для мультивалютного депозита')
        elif currency_score > 0.4:
            reasons.append('Умеренные валютные операции - подходит для диверсификации')
        
        # 3. Анализ потребности в ребалансировке (важный фактор - 15%)
        rebalancing_score = self._analyze_rebalancing_need(client_data)
        score += rebalancing_score * 0.15
        if rebalancing_score > 0.6:
            reasons.append('Потребность в валютной ребалансировке')
        elif rebalancing_score > 0.3:
            reasons.append('Умеренная потребность в диверсификации валют')
        
        # 4. Анализ сберегательного поведения (дополнительный фактор - 10%)
        savings_score = self._analyze_savings_behavior(client_data)
        score += savings_score * 0.1
        if savings_score > 0.6:
            reasons.append('Склонность к сбережениям и накоплениям')
        
        # Нормализуем скор
        final_score = min(score, 1.0)
        
        # Дополнительные проверки на основе исследований
        if avg_balance < 500000:  # Менее 500 тыс
            final_score *= 0.2
            reasons.append('Недостаточный баланс для мультивалютного депозита')
        elif avg_balance < 1000000:  # Менее 1 млн
            final_score *= 0.6
            reasons.append('Баланс ниже рекомендуемого для мультивалютного депозита')
        
        # Бонус за высокую валютную активность
        if hasattr(self, 'currency_activity_data') and self.currency_activity_data:
            currency_ratio = self.currency_activity_data.get('currency_ratio', 0)
            if currency_ratio >= 0.3:  # 30%+ валютных операций
                final_score = min(final_score * 1.2, 1.0)
                reasons.append('Бонус за высокую валютную активность')
        
        expected_benefit = self.calculate_expected_benefit(client_data, final_score)
        
        return self.format_analysis_result(final_score, reasons, expected_benefit)
    
    def _analyze_financial_stability(self, avg_balance: float, status: str) -> float:
        """Анализ финансовой стабильности для мультивалютного депозита"""
        # Базовый скор по балансу
        if avg_balance >= 5000000:  # 5+ млн - отлично
            base_score = 1.0
        elif avg_balance >= 2000000:  # 2-5 млн - хорошо
            base_score = 0.8
        elif avg_balance >= 1000000:  # 1-2 млн - удовлетворительно
            base_score = 0.6
        elif avg_balance >= 500000:  # 500 тыс - 1 млн - слабо
            base_score = 0.4
        else:  # Менее 500 тыс - плохо
            base_score = 0.1
        
        # Бонус за статус клиента
        status_bonus = 0.0
        if status == 'Премиальный клиент':
            status_bonus = 0.2
        elif status == 'Зарплатный клиент':
            status_bonus = 0.1
        elif status == 'Стандартный клиент':
            status_bonus = 0.05
        
        return min(base_score + status_bonus, 1.0)
    
    def _analyze_currency_activity(self, client_data: Dict) -> float:
        """Анализ валютной активности по официальным типам переводов"""
        transfers = client_data.get('transfers', [])
        transactions = client_data.get('transactions', [])
        
        # Официальные типы валютных операций из БД
        currency_transfer_types = ['fx_buy', 'fx_sell', 'deposit_fx_topup_out', 'deposit_fx_withdraw_in']
        
        currency_operations = 0
        total_operations = len(transfers) + len(transactions)
        
        # Анализируем переводы по официальным типам
        for transfer in transfers:
            transfer_type = transfer.get('type', '')
            currency = transfer.get('currency', '')
            
            # Проверяем официальные типы валютных операций
            if transfer_type in currency_transfer_types:
                currency_operations += 1
            # Проверяем валюту (не KZT)
            elif currency and currency.upper() != 'KZT':
                currency_operations += 1
        
        # Анализируем транзакции по валюте
        for transaction in transactions:
            currency = transaction.get('currency', '')
            if currency and currency.upper() != 'KZT':
                currency_operations += 1
        
        if total_operations == 0:
            return 0.0
        
        currency_ratio = currency_operations / total_operations
        
        # Сохраняем данные для анализа
        self.currency_activity_data = {
            'currency_operations': currency_operations,
            'total_operations': total_operations,
            'currency_ratio': currency_ratio
        }
        
        # Оцениваем по доле валютных операций
        if currency_ratio >= 0.3:  # 30%+ валютных операций
            return 1.0
        elif currency_ratio >= 0.2:  # 20-30%
            return 0.8
        elif currency_ratio >= 0.1:  # 10-20%
            return 0.6
        elif currency_ratio >= 0.05:  # 5-10%
            return 0.4
        else:
            return 0.1
    
    def _analyze_rebalancing_need(self, client_data: Dict) -> float:
        """Анализ потребности в валютной ребалансировке"""
        transfers = client_data.get('transfers', [])
        
        # Официальные типы операций, указывающие на потребность в ребалансировке
        rebalancing_types = ['fx_buy', 'fx_sell', 'deposit_fx_topup_out', 'deposit_fx_withdraw_in']
        
        rebalancing_operations = 0
        total_transfers = len(transfers)
        
        for transfer in transfers:
            transfer_type = transfer.get('type', '')
            if transfer_type in rebalancing_types:
                rebalancing_operations += 1
        
        if total_transfers == 0:
            return 0.0
        
        rebalancing_ratio = rebalancing_operations / total_transfers
        
        # Оцениваем потребность в ребалансировке
        if rebalancing_ratio >= 0.2:  # 20%+ операций ребалансировки
            return 1.0
        elif rebalancing_ratio >= 0.1:  # 10-20%
            return 0.7
        elif rebalancing_ratio >= 0.05:  # 5-10%
            return 0.4
        else:
            return 0.1
    
    def _analyze_savings_behavior(self, client_data: Dict) -> float:
        """Анализ сберегательного поведения по официальным типам переводов"""
        transfers = client_data.get('transfers', [])
        
        # Официальные типы операций, указывающие на сберегательное поведение
        savings_types = ['deposit_topup_out', 'deposit_fx_topup_out', 'invest_in']
        
        savings_operations = 0
        
        for transfer in transfers:
            transfer_type = transfer.get('type', '')
            if transfer_type in savings_types:
                savings_operations += 1
        
        # Оцениваем по количеству операций
        if savings_operations >= 5:
            return 1.0
        elif savings_operations >= 3:
            return 0.7
        elif savings_operations >= 1:
            return 0.4
        else:
            return 0.1
    
    def calculate_expected_benefit(self, client_data: Dict, score: float) -> float:
        """Расчет ожидаемой выгоды от мультивалютного депозита"""
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Базовая выгода от процентной ставки
        base_benefit = avg_balance * self.conditions['interest_rate']  # 14.50%
        
        # Дополнительная выгода от валютной диверсификации
        diversification_benefit = avg_balance * 0.02  # 2% за диверсификацию
        
        # Бонус за гибкость (пополнение и снятие без ограничений)
        flexibility_benefit = avg_balance * 0.01  # 1% за гибкость
        
        total_benefit = (base_benefit + diversification_benefit + flexibility_benefit) * score
        
        return total_benefit
