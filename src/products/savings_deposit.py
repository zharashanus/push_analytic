"""
Сценарий для сберегательного депозита
Основан на авторитетных исследованиях сберегательного поведения и защиты депозитов
"""

from typing import Dict, List, Any
from .base_scenario_fixed import BaseProductScenario


class SavingsDepositScenario(BaseProductScenario):
    """Сценарий для сберегательного депозита"""
    
    def __init__(self):
        super().__init__()
        self.product_name = "Депозит Сберегательный"
        self.category = "deposits"
        self.description = "16.50% ставка, защита KDIF, без пополнения и снятия до конца срока"
        self.target_audience = "Клиенты для максимального дохода при готовности заморозить средства"
        
        # Условия основаны на исследованиях сберегательного поведения
        self.conditions = {
            'min_balance': 2000000,  # 2 млн тенге (финансовая стабильность)
            'interest_rate': 0.165,  # 16.50% годовых
            'kdif_protection': True,  # Защита KDIF
            'no_deposits': True,  # Без пополнения
            'no_withdrawals': True,  # Без снятия до конца срока
            'min_age': 18,  # Минимальный возраст
            'max_age': 70,  # Максимальный возраст
            'min_balance_stability': 0.8  # 80% стабильности баланса
        }
        
        # Преимущества согласно требованиям
        self.benefits = {
            'interest_rate': 0.165,  # 16.50% годовых (максимальная ставка)
            'kdif_protection': True,  # Защита KDIF до 20 млн тенге
            'maximum_return': True,  # Максимальный доход
            'guaranteed_income': True,  # Гарантированный доход
            'risk_free': True,  # Безрисковый инструмент
            'long_term_growth': True  # Долгосрочный рост капитала
        }
    
    def analyze_client(self, client_code: str, days: int, db_manager) -> Dict[str, Any]:
        """
        Анализ соответствия клиента сберегательному депозиту
        Основан на исследованиях сберегательного поведения и защиты депозитов
        """
        client_data = self.get_client_data(client_code, days, db_manager)
        if not client_data:
            return self.format_analysis_result(0, ['Клиент не найден'], 0)
        
        reasons = []
        score = 0.0
        
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        status = client_info.get('status', '')
        
        # 1. Анализ финансовой стабильности (основной критерий - 50%)
        stability_score = self._analyze_financial_stability(avg_balance, status)
        score += stability_score * 0.5
        if stability_score > 0.8:
            reasons.append('Высокая финансовая стабильность для сберегательного депозита')
        elif stability_score > 0.5:
            reasons.append('Достаточная финансовая стабильность')
        
        # 2. Анализ готовности к заморозке средств (ключевой фактор - 30%)
        freeze_readiness_score = self._analyze_freeze_readiness(client_data)
        score += freeze_readiness_score * 0.3
        if freeze_readiness_score > 0.7:
            reasons.append('Готовность к заморозке средств на длительный срок')
        elif freeze_readiness_score > 0.4:
            reasons.append('Умеренная готовность к долгосрочным вложениям')
        
        # 3. Анализ сберегательного поведения (важный фактор - 15%)
        savings_score = self._analyze_savings_behavior(client_data)
        score += savings_score * 0.15
        if savings_score > 0.6:
            reasons.append('Склонность к долгосрочным сбережениям и накоплениям')
        elif savings_score > 0.3:
            reasons.append('Умеренная склонность к сбережениям')
        
        # 4. Анализ статуса клиента (дополнительный фактор - 5%)
        status_score = self._analyze_status_suitability(status)
        score += status_score * 0.05
        if status_score > 0.7:
            reasons.append('Оптимальный статус для долгосрочных сбережений')
        elif status_score > 0.4:
            reasons.append('Подходящий статус для сберегательного депозита')
        
        # Нормализуем скор
        final_score = min(score, 1.0)
        
        # Дополнительные проверки на основе исследований
        if avg_balance < 1000000:  # Менее 1 млн
            final_score *= 0.1
            reasons.append('Недостаточный баланс для сберегательного депозита')
        elif avg_balance < 2000000:  # Менее 2 млн
            final_score *= 0.5
            reasons.append('Баланс ниже рекомендуемого для сберегательного депозита')
        
        # Проверка статуса клиента
        if status not in ['Премиальный клиент', 'Зарплатный клиент', 'Стандартный клиент', 'Студент']:
            final_score *= 0.3
            reasons.append('Статус не соответствует требованиям сберегательного депозита')
        
        # Бонус за высокую стабильность баланса
        if hasattr(self, 'balance_stability_data') and self.balance_stability_data:
            stability_ratio = self.balance_stability_data.get('stability_ratio', 0)
            if stability_ratio >= 0.8:  # 80%+ стабильности
                final_score = min(final_score * 1.15, 1.0)
                reasons.append('Бонус за высокую стабильность баланса')
        
        expected_benefit = self.calculate_expected_benefit(client_data, final_score)
        
        return self.format_analysis_result(final_score, reasons, expected_benefit)
    
    def _analyze_financial_stability(self, avg_balance: float, status: str) -> float:
        """Анализ финансовой стабильности для сберегательного депозита"""
        # Базовый скор по балансу
        if avg_balance >= 10000000:  # 10+ млн - отлично
            base_score = 1.0
        elif avg_balance >= 5000000:  # 5-10 млн - очень хорошо
            base_score = 0.9
        elif avg_balance >= 2000000:  # 2-5 млн - хорошо
            base_score = 0.7
        elif avg_balance >= 1000000:  # 1-2 млн - удовлетворительно
            base_score = 0.4
        else:  # Менее 1 млн - плохо
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
    
    def _analyze_freeze_readiness(self, client_data: Dict) -> float:
        """Анализ готовности к заморозке средств"""
        transfers = client_data.get('transfers', [])
        transactions = client_data.get('transactions', [])
        
        # Анализируем стабильность баланса
        balance_stability = self._analyze_balance_stability(client_data)
        
        # Анализируем отсутствие частых снятий
        withdrawal_frequency = self._analyze_withdrawal_frequency(transfers)
        
        # Анализируем долгосрочные вложения
        long_term_investments = self._analyze_long_term_investments(transfers)
        
        # Комбинируем оценки
        return (balance_stability + withdrawal_frequency + long_term_investments) / 3
    
    def _analyze_balance_stability(self, client_data: Dict) -> float:
        """Анализ стабильности баланса"""
        # Упрощенный анализ - в реальности нужны данные по месяцам
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Предполагаем стабильность на основе размера баланса
        if avg_balance >= 5000000:  # 5+ млн - высокая стабильность
            stability_ratio = 0.9
        elif avg_balance >= 2000000:  # 2-5 млн - средняя стабильность
            stability_ratio = 0.7
        elif avg_balance >= 1000000:  # 1-2 млн - низкая стабильность
            stability_ratio = 0.5
        else:
            stability_ratio = 0.2
        
        # Сохраняем данные для анализа
        self.balance_stability_data = {
            'stability_ratio': stability_ratio,
            'avg_balance': avg_balance
        }
        
        return stability_ratio
    
    def _analyze_withdrawal_frequency(self, transactions: List[Dict]) -> float:
        """Анализ частоты снятий"""
        if not transactions:
            return 0.5  # Нейтральная оценка при отсутствии данных
        
        # Считаем операции снятия (упрощенно)
        withdrawal_operations = 0
        for transaction in transactions:
            amount = float(transaction.get('amount', 0))
            if amount < 0:  # Предполагаем, что отрицательные суммы - снятия
                withdrawal_operations += 1
        
        total_operations = len(transactions)
        withdrawal_ratio = withdrawal_operations / total_operations if total_operations > 0 else 0
        
        # Низкая частота снятий = высокая готовность к заморозке
        if withdrawal_ratio <= 0.1:  # ≤10% снятий
            return 1.0
        elif withdrawal_ratio <= 0.2:  # ≤20% снятий
            return 0.8
        elif withdrawal_ratio <= 0.3:  # ≤30% снятий
            return 0.6
        else:
            return 0.3
    
    def _analyze_long_term_investments(self, transfers: List[Dict]) -> float:
        """Анализ долгосрочных вложений"""
        # Официальные типы операций, указывающие на долгосрочные вложения
        long_term_types = ['deposit_topup_out', 'invest_in', 'deposit_fx_topup_out']
        
        long_term_operations = 0
        for transfer in transfers:
            transfer_type = transfer.get('type', '')
            if transfer_type in long_term_types:
                long_term_operations += 1
        
        # Оцениваем по количеству долгосрочных операций
        if long_term_operations >= 5:
            return 1.0
        elif long_term_operations >= 3:
            return 0.7
        elif long_term_operations >= 1:
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
    
    def _analyze_status_suitability(self, status: str) -> float:
        """Анализ подходящего статуса для сберегательного депозита"""
        if status == 'Премиальный клиент':
            return 1.0
        elif status == 'Зарплатный клиент':
            return 0.8
        elif status == 'Стандартный клиент':
            return 0.6
        elif status == 'Студент':
            return 0.3
        else:
            return 0.2
    
    def calculate_expected_benefit(self, client_data: Dict, score: float) -> float:
        """Расчет ожидаемой выгоды от сберегательного депозита"""
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Базовая выгода от максимальной процентной ставки
        base_benefit = avg_balance * self.conditions['interest_rate']  # 16.50%
        
        # Дополнительная выгода от защиты KDIF
        kdif_benefit = avg_balance * 0.01  # 1% за защиту KDIF
        
        # Бонус за максимальный доход
        max_return_bonus = avg_balance * 0.02  # 2% за максимальный доход
        
        total_benefit = (base_benefit + kdif_benefit + max_return_bonus) * score
        
        return total_benefit
