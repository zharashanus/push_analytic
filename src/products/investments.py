"""
Сценарий для инвестиций
Основан на авторитетных исследованиях инвестиционного поведения и финансовой грамотности
"""

from typing import Dict, List, Any
from .base_scenario_fixed import BaseProductScenario


class InvestmentsScenario(BaseProductScenario):
    """Сценарий для инвестиций"""
    
    def __init__(self):
        super().__init__()
        self.product_name = "Инвестиции"
        self.category = "investments"
        self.description = "0% комиссии на сделки, от 6 ₸, без комиссий в первый год"
        self.target_audience = "Клиенты для старта с малых сумм и без издержек на входе"
        
        # Условия основаны на исследованиях инвестиционного поведения
        self.conditions = {
            'min_investment': 6,  # 6 тенге (минимальный порог входа)
            'commission_rate': 0.0,  # 0% комиссия на сделки
            'first_year_free': True,  # Без комиссий в первый год
            'min_balance': 100000,  # 100 тыс тенге (базовый уровень)
            'min_age': 18,  # Минимальный возраст
            'max_age': 70,  # Максимальный возраст
            'min_financial_literacy': 0.3  # 30% финансовая грамотность
        }
        
        # Преимущества согласно требованиям
        self.benefits = {
            'zero_commission': True,  # 0% комиссии на сделки
            'minimal_entry': 6,  # Минимальный порог входа от 6 ₸
            'first_year_free': True,  # Без комиссий в первый год
            'low_barrier': True,  # Низкий барьер входа
            'cost_efficiency': True,  # Эффективность по затратам
            'accessibility': True  # Доступность для всех
        }
    
    def analyze_client(self, client_code: str, days: int, db_manager) -> Dict[str, Any]:
        """
        Анализ соответствия клиента инвестициям
        Основан на исследованиях инвестиционного поведения и финансовой грамотности
        """
        client_data = self.get_client_data(client_code, days, db_manager)
        if not client_data:
            return self.format_analysis_result(0, ['Клиент не найден'], 0)
        
        reasons = []
        score = 0.0
        
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        status = client_info.get('status', '')
        
        # 1. Анализ финансовой готовности (основной критерий - 30%)
        readiness_score = self._analyze_investment_readiness(avg_balance, status)
        score += readiness_score * 0.3
        if readiness_score > 0.7:
            reasons.append('Финансовая готовность к инвестициям')
        elif readiness_score > 0.4:
            reasons.append('Базовая финансовая готовность')
        
        # 2. Анализ инвестиционного потенциала (ключевой фактор - 35%)
        potential_score = self._analyze_investment_potential(client_data)
        score += potential_score * 0.35
        if potential_score > 0.7:
            reasons.append('Высокий инвестиционный потенциал')
        elif potential_score > 0.4:
            reasons.append('Умеренный инвестиционный потенциал')
        
        # 3. Анализ готовности к риску (важный фактор - 20%)
        risk_score = self._analyze_risk_tolerance(client_data)
        score += risk_score * 0.2
        if risk_score > 0.6:
            reasons.append('Готовность к инвестиционным рискам')
        elif risk_score > 0.3:
            reasons.append('Умеренная готовность к риску')
        
        # 4. Анализ статуса клиента (дополнительный фактор - 15%)
        status_score = self._analyze_status_suitability(status)
        score += status_score * 0.15
        if status_score > 0.7:
            reasons.append('Оптимальный статус для начала инвестиций')
        elif status_score > 0.4:
            reasons.append('Подходящий статус для инвестиций')
        
        # Нормализуем скор
        final_score = min(score, 1.0)
        
        # Дополнительные проверки на основе исследований
        if avg_balance < 50000:  # Менее 50 тыс
            final_score *= 0.3
            reasons.append('Недостаточные средства для инвестиций')
        elif avg_balance < 100000:  # Менее 100 тыс
            final_score *= 0.7
            reasons.append('Минимальные средства для инвестиций')
        
        # Проверка статуса клиента
        if status not in ['Премиальный клиент', 'Зарплатный клиент', 'Стандартный клиент', 'Студент']:
            final_score *= 0.2
            reasons.append('Статус не соответствует требованиям для инвестиций')
        
        # Бонус за низкий барьер входа (от 6 ₸)
        if avg_balance >= 100000:  # 100+ тыс
            final_score = min(final_score * 1.1, 1.0)
            reasons.append('Бонус за доступность инвестиций от 6 ₸')
        
        expected_benefit = self.calculate_expected_benefit(client_data, final_score)
        
        return self.format_analysis_result(final_score, reasons, expected_benefit)
    
    def _analyze_investment_readiness(self, avg_balance: float, status: str) -> float:
        """Анализ финансовой готовности к инвестициям"""
        # Базовый скор по балансу
        if avg_balance >= 2000000:  # 2+ млн - отлично
            base_score = 1.0
        elif avg_balance >= 1000000:  # 1-2 млн - хорошо
            base_score = 0.8
        elif avg_balance >= 500000:  # 500 тыс - 1 млн - удовлетворительно
            base_score = 0.6
        elif avg_balance >= 100000:  # 100-500 тыс - слабо
            base_score = 0.4
        else:  # Менее 100 тыс - плохо
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
    
    def _analyze_investment_potential(self, client_data: Dict) -> float:
        """Анализ инвестиционного потенциала по официальным типам переводов"""
        transfers = client_data.get('transfers', [])
        transactions = client_data.get('transactions', [])
        
        # Официальные типы операций, указывающие на инвестиционный потенциал
        investment_types = ['invest_in', 'invest_out', 'deposit_topup_out', 'deposit_fx_topup_out']
        
        investment_operations = 0
        total_amount = 0
        
        for transfer in transfers:
            transfer_type = transfer.get('type', '')
            amount = float(transfer.get('amount', 0))
            
            if transfer_type in investment_types:
                investment_operations += 1
                total_amount += amount
        
        # Анализируем разнообразие транзакций (показатель финансовой активности)
        categories = set()
        for transaction in transactions:
            category = transaction.get('category', '')
            if category:
                categories.add(category)
        
        # Оцениваем по количеству инвестиционных операций
        operations_score = 0.0
        if investment_operations >= 5:
            operations_score = 1.0
        elif investment_operations >= 3:
            operations_score = 0.8
        elif investment_operations >= 1:
            operations_score = 0.6
        else:
            operations_score = 0.2
        
        # Оцениваем по разнообразию транзакций
        diversity_score = 0.0
        if len(categories) >= 8:
            diversity_score = 1.0
        elif len(categories) >= 5:
            diversity_score = 0.8
        elif len(categories) >= 3:
            diversity_score = 0.6
        elif len(categories) >= 2:
            diversity_score = 0.4
        else:
            diversity_score = 0.1
        
        return (operations_score + diversity_score) / 2
    
    def _analyze_risk_tolerance(self, client_data: Dict) -> float:
        """Анализ готовности к инвестиционным рискам"""
        transfers = client_data.get('transfers', [])
        transactions = client_data.get('transactions', [])
        
        # Официальные типы операций, указывающие на готовность к риску
        risk_types = ['invest_in', 'invest_out', 'fx_buy', 'fx_sell', 'gold_buy_out', 'gold_sell_in']
        
        risk_operations = 0
        for transfer in transfers:
            transfer_type = transfer.get('type', '')
            if transfer_type in risk_types:
                risk_operations += 1
        
        # Анализируем активность транзакций (показатель готовности к действиям)
        transaction_activity = len(transactions)
        
        # Оцениваем по количеству рискованных операций
        risk_score = 0.0
        if risk_operations >= 3:
            risk_score = 1.0
        elif risk_operations >= 2:
            risk_score = 0.8
        elif risk_operations >= 1:
            risk_score = 0.6
        else:
            risk_score = 0.2
        
        # Оцениваем по активности транзакций
        activity_score = 0.0
        if transaction_activity >= 30:
            activity_score = 1.0
        elif transaction_activity >= 20:
            activity_score = 0.8
        elif transaction_activity >= 10:
            activity_score = 0.6
        elif transaction_activity >= 5:
            activity_score = 0.4
        else:
            activity_score = 0.1
        
        return (risk_score + activity_score) / 2
    
    def _analyze_status_suitability(self, status: str) -> float:
        """Анализ подходящего статуса для инвестиций"""
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
        """Расчет ожидаемой выгоды от инвестиций"""
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Базовая выгода от инвестиций (консервативная оценка)
        base_benefit = avg_balance * 0.05  # 5% потенциальный доход
        
        # Дополнительная выгода от нулевых комиссий
        commission_benefit = avg_balance * 0.01  # 1% экономия на комиссиях
        
        # Бонус за низкий барьер входа
        accessibility_bonus = avg_balance * 0.005  # 0.5% за доступность
        
        total_benefit = (base_benefit + commission_benefit + accessibility_bonus) * score
        
        return total_benefit
