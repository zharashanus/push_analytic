"""
Сценарий для накопительного депозита
Основан на авторитетных исследованиях накопительного поведения и планомерного сбережения
"""

from typing import Dict, List, Any
from .base_scenario_fixed import BaseProductScenario


class AccumulationDepositScenario(BaseProductScenario):
    """Сценарий для накопительного депозита"""
    
    def __init__(self):
        super().__init__()
        self.product_name = "Депозит Накопительный"
        self.category = "deposits"
        self.description = "15.50% ставка, пополнение да, снятие нет"
        self.target_audience = "Клиенты для планомерного откладывания под повышенную ставку"
        
        # Условия основаны на исследованиях накопительного поведения
        self.conditions = {
            'min_balance': 500000,  # 500 тыс тенге (базовый уровень)
            'interest_rate': 0.155,  # 15.50% годовых
            'can_deposit': True,  # Пополнение разрешено
            'no_withdrawals': True,  # Снятие запрещено
            'min_regular_deposits': 2,  # Минимум 2 пополнения в месяц
            'min_age': 18,  # Минимальный возраст
            'max_age': 70,  # Максимальный возраст
            'min_savings_ratio': 0.1  # 10% от дохода на сбережения
        }
        
        # Преимущества согласно требованиям
        self.benefits = {
            'interest_rate': 0.155,  # 15.50% годовых (повышенная ставка)
            'can_deposit': True,  # Возможность пополнения
            'gradual_savings': True,  # Планомерное накопление
            'higher_rate': True,  # Повышенная ставка за накопления
            'discipline': True,  # Финансовая дисциплина
            'goal_achievement': True  # Достижение финансовых целей
        }
    
    def analyze_client(self, client_code: str, days: int, db_manager) -> Dict[str, Any]:
        """
        Анализ соответствия клиента накопительному депозиту
        Основан на исследованиях накопительного поведения и планомерного сбережения
        """
        client_data = self.get_client_data(client_code, days, db_manager)
        if not client_data:
            return self.format_analysis_result(0, ['Клиент не найден'], 0)
        
        reasons = []
        score = 0.0
        
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        status = client_info.get('status', '')
        
        # 1. Анализ финансовой стабильности (основной критерий - 35%)
        stability_score = self._analyze_financial_stability(avg_balance, status)
        score += stability_score * 0.35
        if stability_score > 0.7:
            reasons.append('Стабильный доход для планомерного накопления')
        elif stability_score > 0.4:
            reasons.append('Достаточная финансовая стабильность')
        
        # 2. Анализ накопительного поведения (ключевой фактор - 40%)
        accumulation_score = self._analyze_accumulation_behavior(client_data)
        score += accumulation_score * 0.4
        if accumulation_score > 0.7:
            reasons.append('Активное накопительное поведение - идеально для накопительного депозита')
        elif accumulation_score > 0.4:
            reasons.append('Умеренная склонность к накоплениям')
        
        # 3. Анализ регулярности пополнений (важный фактор - 15%)
        regularity_score = self._analyze_deposit_regularity(client_data)
        score += regularity_score * 0.15
        if regularity_score > 0.6:
            reasons.append('Регулярные пополнения - подходит для накопительного депозита')
        elif regularity_score > 0.3:
            reasons.append('Умеренная регулярность пополнений')
        
        # 4. Анализ статуса клиента (дополнительный фактор - 10%)
        status_score = self._analyze_status_suitability(status)
        score += status_score * 0.1
        if status_score > 0.7:
            reasons.append('Оптимальный статус для планомерного накопления')
        elif status_score > 0.4:
            reasons.append('Подходящий статус для накопительного депозита')
        
        # Нормализуем скор
        final_score = min(score, 1.0)
        
        # Дополнительные проверки на основе исследований
        if avg_balance < 200000:  # Менее 200 тыс
            final_score *= 0.2
            reasons.append('Недостаточный доход для планомерного накопления')
        elif avg_balance < 500000:  # Менее 500 тыс
            final_score *= 0.6
            reasons.append('Доход ниже рекомендуемого для накопительного депозита')
        
        # Проверка статуса клиента
        if status not in ['Премиальный клиент', 'Зарплатный клиент', 'Стандартный клиент', 'Студент']:
            final_score *= 0.3
            reasons.append('Статус не соответствует требованиям накопительного депозита')
        
        # Бонус за высокую накопительную активность
        if hasattr(self, 'accumulation_data') and self.accumulation_data:
            deposit_frequency = self.accumulation_data.get('deposit_frequency', 0)
            if deposit_frequency >= 2:  # 2+ пополнения в месяц
                final_score = min(final_score * 1.2, 1.0)
                reasons.append('Бонус за высокую накопительную активность')
        
        expected_benefit = self.calculate_expected_benefit(client_data, final_score)
        
        return self.format_analysis_result(final_score, reasons, expected_benefit)
    
    def _analyze_financial_stability(self, avg_balance: float, status: str) -> float:
        """Анализ финансовой стабильности для накопительного депозита"""
        # Базовый скор по балансу
        if avg_balance >= 2000000:  # 2+ млн - отлично
            base_score = 1.0
        elif avg_balance >= 1000000:  # 1-2 млн - хорошо
            base_score = 0.8
        elif avg_balance >= 500000:  # 500 тыс - 1 млн - удовлетворительно
            base_score = 0.6
        elif avg_balance >= 200000:  # 200-500 тыс - слабо
            base_score = 0.4
        else:  # Менее 200 тыс - плохо
            base_score = 0.1
        
        # Бонус за статус клиента
        status_bonus = 0.0
        if status == 'Премиальный клиент':
            status_bonus = 0.2
        elif status == 'Зарплатный клиент':
            status_bonus = 0.15
        elif status == 'Стандартный клиент':
            status_bonus = 0.1
        elif status == 'Студент':
            status_bonus = 0.05
        
        return min(base_score + status_bonus, 1.0)
    
    def _analyze_accumulation_behavior(self, client_data: Dict) -> float:
        """Анализ накопительного поведения по официальным типам переводов"""
        transfers = client_data.get('transfers', [])
        period_days = client_data.get('period_days', 90)
        
        # Официальные типы операций, указывающие на накопительное поведение
        accumulation_types = ['deposit_topup_out', 'deposit_fx_topup_out', 'invest_in']
        
        accumulation_operations = 0
        total_amount = 0
        
        for transfer in transfers:
            transfer_type = transfer.get('type', '')
            amount = float(transfer.get('amount', 0))
            
            if transfer_type in accumulation_types:
                accumulation_operations += 1
                total_amount += amount
        
        # Рассчитываем частоту пополнений в месяц
        monthly_frequency = accumulation_operations / period_days * 30
        
        # Анализируем размер пополнений относительно дохода
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        savings_ratio = total_amount / (avg_balance * 3) if avg_balance > 0 else 0  # 3 месяца
        
        # Сохраняем данные для анализа
        self.accumulation_data = {
            'deposit_frequency': monthly_frequency,
            'savings_ratio': savings_ratio,
            'total_amount': total_amount,
            'operations_count': accumulation_operations
        }
        
        # Оцениваем по частоте пополнений
        frequency_score = 0.0
        if monthly_frequency >= 3:  # 3+ пополнения в месяц
            frequency_score = 1.0
        elif monthly_frequency >= 2:  # 2-3 пополнения
            frequency_score = 0.8
        elif monthly_frequency >= 1:  # 1-2 пополнения
            frequency_score = 0.6
        elif monthly_frequency >= 0.5:  # 0.5-1 пополнение
            frequency_score = 0.4
        else:
            frequency_score = 0.1
        
        # Оцениваем по доле сбережений
        ratio_score = 0.0
        if savings_ratio >= 0.2:  # 20%+ от дохода
            ratio_score = 1.0
        elif savings_ratio >= 0.15:  # 15-20%
            ratio_score = 0.8
        elif savings_ratio >= 0.1:  # 10-15%
            ratio_score = 0.6
        elif savings_ratio >= 0.05:  # 5-10%
            ratio_score = 0.4
        else:
            ratio_score = 0.1
        
        return (frequency_score + ratio_score) / 2
    
    def _analyze_deposit_regularity(self, client_data: Dict) -> float:
        """Анализ регулярности пополнений депозитов"""
        transfers = client_data.get('transfers', [])
        period_days = client_data.get('period_days', 90)
        
        # Официальные типы операций пополнения депозитов
        deposit_types = ['deposit_topup_out', 'deposit_fx_topup_out']
        
        deposit_operations = 0
        for transfer in transfers:
            transfer_type = transfer.get('type', '')
            if transfer_type in deposit_types:
                deposit_operations += 1
        
        # Рассчитываем регулярность (операции в месяц)
        monthly_frequency = deposit_operations / period_days * 30
        
        # Оцениваем регулярность
        if monthly_frequency >= 2:  # 2+ пополнения в месяц
            return 1.0
        elif monthly_frequency >= 1:  # 1-2 пополнения
            return 0.7
        elif monthly_frequency >= 0.5:  # 0.5-1 пополнение
            return 0.4
        else:
            return 0.1
    
    def _analyze_status_suitability(self, status: str) -> float:
        """Анализ подходящего статуса для накопительного депозита"""
        if status == 'Премиальный клиент':
            return 1.0
        elif status == 'Зарплатный клиент':
            return 0.8
        elif status == 'Стандартный клиент':
            return 0.6
        elif status == 'Студент':
            return 0.4
        else:
            return 0.2
    
    def calculate_expected_benefit(self, client_data: Dict, score: float) -> float:
        """Расчет ожидаемой выгоды от накопительного депозита"""
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Базовая выгода от повышенной процентной ставки
        base_benefit = avg_balance * self.conditions['interest_rate']  # 15.50%
        
        # Дополнительная выгода от возможности пополнения
        deposit_benefit = avg_balance * 0.02  # 2% за возможность пополнения
        
        # Бонус за планомерное накопление
        accumulation_bonus = avg_balance * 0.01  # 1% за накопительное поведение
        
        total_benefit = (base_benefit + deposit_benefit + accumulation_bonus) * score
        
        return total_benefit
