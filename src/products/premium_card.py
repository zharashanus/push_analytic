"""
Сценарий для премиальной карты
Основан на исследованиях премиальных банковских продуктов в Казахстане
"""

from typing import Dict, List, Any
from .base_scenario_fixed import BaseProductScenario


class PremiumCardScenario(BaseProductScenario):
    """Сценарий для премиальной карты"""
    
    def __init__(self):
        super().__init__()
        self.product_name = "Премиальная карта"
        self.category = "cards"
        self.description = "2-4% кешбэк, бесплатные снятия до 3 млн/мес, переводы"
        self.target_audience = "Клиенты с высоким балансом и активными операциями"
        
        # Условия основаны на исследованиях премиальных карт в Казахстане
        self.conditions = {
            'min_balance': 800000,  # 800 тыс тенге (основной порог по исследованиям)
            'premium_balance': 1000000,  # 1 млн для повышенного кешбэка
            'vip_balance': 6000000,  # 6 млн для максимального кешбэка
            'min_transfers': 5,  # Минимум 5 переводов в месяц
            'min_transactions': 10,  # Минимум 10 транзакций в месяц
            'premium_categories': ['рестораны', 'парфюмерия', 'подарки', 'ювелирные украшения']
        }
        
        # Преимущества согласно требованиям
        self.benefits = {
            'base_cashback': 0.02,  # 2% базовый кешбэк
            'deposit_1_6m_cashback': 0.03,  # 3% при депозите 1-6 млн
            'deposit_6m_plus_cashback': 0.04,  # 4% при депозите от 6 млн
            'premium_categories_cashback': 0.04,  # 4% на премиальные категории
            'free_withdrawals': 3000000,  # 3 млн бесплатных снятий
            'free_transfers_rk': True,  # Бесплатные переводы на карты РК
            'cashback_limit': 100000  # 100 тыс лимит кешбэка
        }
    
    def analyze_client(self, client_code: str, days: int, db_manager) -> Dict[str, Any]:
        """
        Анализ соответствия клиента премиальной карте
        Основан на исследованиях премиальных банковских продуктов
        """
        client_data = self.get_client_data(client_code, days, db_manager)
        if not client_data:
            return self.format_analysis_result(0, ['Клиент не найден'], 0)
        
        reasons = []
        score = 0.0
        
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        client_status = client_info.get('status', '').lower()
        
        # 1. Анализ баланса (основной критерий по исследованиям)
        balance_score = self._analyze_balance(avg_balance)
        score += balance_score * 0.4
        if balance_score > 0.9:
            reasons.append('Очень высокий баланс - идеально для премиальной карты')
        elif balance_score > 0.7:
            reasons.append('Высокий баланс - отлично подходит для премиальной карты')
        elif balance_score > 0.5:
            reasons.append('Достаточный баланс для премиальной карты')
        
        # 2. Анализ статуса клиента (официальный статус)
        status_score = self._analyze_client_status(client_status)
        score += status_score * 0.2
        if status_score > 0.8:
            reasons.append('Премиальный статус клиента')
        elif status_score > 0.5:
            reasons.append('Подходящий статус клиента')
        
        # 3. Анализ премиальных трат (рестораны, парфюмерия, подарки, ювелир)
        premium_spending_score = self._analyze_premium_spending(client_data)
        score += premium_spending_score * 0.2
        if premium_spending_score > 0.7:
            reasons.append('Активные траты в премиальных категориях')
        elif premium_spending_score > 0.4:
            reasons.append('Умеренные траты в премиальных категориях')
        
        # 4. Анализ поступлений (зарплата, p2p)
        income_score = self._analyze_income_patterns(client_data)
        score += income_score * 0.1
        if income_score > 0.7:
            reasons.append('Регулярные крупные поступления')
        elif income_score > 0.4:
            reasons.append('Стабильные поступления')
        
        # 5. Анализ активности операций
        activity_score = self._analyze_activity(client_data)
        score += activity_score * 0.1
        if activity_score > 0.7:
            reasons.append('Высокая активность операций')
        elif activity_score > 0.4:
            reasons.append('Умеренная активность операций')
        
        # Нормализуем скор
        final_score = min(score, 1.0)
        
        # Дополнительные проверки на основе исследований
        if avg_balance < 500000:  # Менее 500 тыс
            final_score *= 0.3
            reasons.append('Недостаточный баланс для премиальной карты')
        elif avg_balance < 800000:  # Менее 800 тыс (основной порог)
            final_score *= 0.6
            reasons.append('Баланс ниже рекомендуемого для премиальной карты')
        
        # Бонус за премиальный статус
        if 'премиальный' in client_status:
            final_score = min(final_score * 1.2, 1.0)
            reasons.append('Бонус за премиальный статус клиента')
        
        expected_benefit = self.calculate_expected_benefit(client_data, final_score)
        
        return self.format_analysis_result(final_score, reasons, expected_benefit)
    
    def _analyze_balance(self, avg_balance: float) -> float:
        """Анализ баланса клиента на основе исследований"""
        if avg_balance >= 6000000:  # 6+ млн - максимальный кешбэк
            return 1.0
        elif avg_balance >= 1000000:  # 1-6 млн - повышенный кешбэк
            return 0.9
        elif avg_balance >= 800000:  # 800+ тыс - основной порог
            return 0.8
        elif avg_balance >= 500000:  # 500-800 тыс - минимальный порог
            return 0.6
        elif avg_balance >= 200000:  # 200-500 тыс - слабо
            return 0.3
        else:  # Менее 200 тыс - плохо
            return 0.1
    
    def _analyze_client_status(self, status: str) -> float:
        """Анализ официального статуса клиента"""
        status_lower = status.lower()
        
        if 'премиальный' in status_lower:
            return 1.0
        elif 'зарплатный' in status_lower:
            return 0.7
        elif 'стандартный' in status_lower:
            return 0.4
        elif 'студент' in status_lower:
            return 0.2
        else:
            return 0.5  # Неизвестный статус - нейтрально
    
    def _analyze_premium_spending(self, client_data: Dict) -> float:
        """Анализ трат в премиальных категориях"""
        transactions = client_data.get('transactions', [])
        if not transactions:
            return 0.0
        
        # Премиальные категории (только официальные категории)
        premium_categories = [
            'Кафе и рестораны', 'Косметика и Парфюмерия', 
            'Подарки', 'Ювелирные украшения'
        ]
        
        total_amount = 0
        premium_amount = 0
        premium_transactions = []
        
        for transaction in transactions:
            amount = float(transaction.get('amount', 0))
            category = transaction.get('category', '')
            
            total_amount += amount
            
            # Проверяем только по официальным категориям
            if category in premium_categories:
                premium_amount += amount
                premium_transactions.append({
                    'amount': amount,
                    'category': category,
                    'date': transaction.get('date')
                })
        
        if total_amount == 0:
            return 0.0
        
        premium_ratio = premium_amount / total_amount
        
        # Сохраняем данные для уведомлений
        self.premium_spending_data = {
            'total_amount': total_amount,
            'premium_amount': premium_amount,
            'premium_ratio': premium_ratio,
            'premium_transactions': premium_transactions,
            'potential_cashback': premium_amount * self.benefits['premium_categories_cashback']
        }
        
        # Оцениваем по доле премиальных трат
        if premium_ratio >= 0.3:  # 30%+ премиальных трат
            return 1.0
        elif premium_ratio >= 0.2:  # 20-30%
            return 0.8
        elif premium_ratio >= 0.1:  # 10-20%
            return 0.6
        elif premium_ratio >= 0.05:  # 5-10%
            return 0.4
        else:
            return 0.2
    
    def _analyze_income_patterns(self, client_data: Dict) -> float:
        """Анализ поступлений (зарплата, p2p)"""
        transfers = client_data.get('transfers', [])
        if not transfers:
            return 0.0
        
        # Типы поступлений
        income_types = ['salary_in', 'stipend_in', 'family_in', 'card_in']
        
        total_income = 0
        income_count = 0
        salary_amount = 0
        p2p_amount = 0
        
        for transfer in transfers:
            transfer_type = transfer.get('type', '').lower()
            direction = transfer.get('direction', '').lower()
            amount = float(transfer.get('amount', 0))
            
            if direction == 'in' and transfer_type in income_types:
                total_income += amount
                income_count += 1
                
                if transfer_type == 'salary_in':
                    salary_amount += amount
                elif transfer_type == 'card_in':
                    p2p_amount += amount
        
        if total_income == 0:
            return 0.0
        
        # Рассчитываем средний размер поступления
        avg_income = total_income / income_count if income_count > 0 else 0
        
        # Оцениваем по размеру и регулярности поступлений
        score = 0.0
        
        # Бонус за крупные поступления
        if avg_income >= 500000:  # 500+ тыс за поступление
            score += 0.5
        elif avg_income >= 200000:  # 200+ тыс
            score += 0.3
        elif avg_income >= 100000:  # 100+ тыс
            score += 0.1
        
        # Бонус за регулярность
        if income_count >= 3:  # 3+ поступления за период
            score += 0.3
        elif income_count >= 1:
            score += 0.1
        
        # Бонус за зарплатные поступления
        if salary_amount > 0:
            score += 0.2
        
        return min(score, 1.0)
    
    def _analyze_activity(self, client_data: Dict) -> float:
        """Анализ активности операций"""
        transactions = client_data.get('transactions', [])
        transfers = client_data.get('transfers', [])
        period_days = client_data.get('period_days', 90)
        
        # Рассчитываем активность в месяц
        monthly_transactions = len(transactions) / period_days * 30
        monthly_transfers = len(transfers) / period_days * 30
        
        # Оцениваем активность
        if monthly_transactions >= 20 and monthly_transfers >= 10:
            return 1.0
        elif monthly_transactions >= 15 and monthly_transfers >= 5:
            return 0.8
        elif monthly_transactions >= 10 and monthly_transfers >= 3:
            return 0.6
        elif monthly_transactions >= 5:
            return 0.4
        else:
            return 0.2
    
    def calculate_expected_benefit(self, client_data: Dict, score: float) -> float:
        """Расчет ожидаемой выгоды с учетом премиальных категорий"""
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Базовая выгода от кешбэка
        base_benefit = avg_balance * 0.02  # 2% базовый кешбэк
        
        # Дополнительная выгода от премиальных категорий
        if hasattr(self, 'premium_spending_data') and self.premium_spending_data:
            premium_benefit = self.premium_spending_data.get('potential_cashback', 0)
            base_benefit += premium_benefit
        
        # Учитываем уровень депозита для повышенного кешбэка
        if avg_balance >= 6000000:
            base_benefit *= 1.5  # 4% вместо 2%
        elif avg_balance >= 1000000:
            base_benefit *= 1.25  # 3% вместо 2%
        
        return base_benefit * score
