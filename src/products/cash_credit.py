"""
Сценарий для кредита наличными
Основан на авторитетных исследованиях потребительского кредитования и финансового поведения
"""

from typing import Dict, List, Any
from .base_scenario_fixed import BaseProductScenario


class CashCreditScenario(BaseProductScenario):
    """Сценарий для кредита наличными"""
    
    def __init__(self):
        super().__init__()
        self.product_name = "Кредит наличными"
        self.category = "loans"
        self.description = "Кредит без залога и справок, 12% на 1 год, 21% свыше года, досрочное погашение без штрафов"
        self.target_audience = "Клиенты, нуждающиеся в быстром финансировании без обеспечения"
        
        # Условия основаны на исследованиях потребительского кредитования
        self.conditions = {
            'min_balance': 300000,  # 300 тыс тенге (финансовая стабильность)
            'min_monthly_income': 200000,  # 200 тыс доход в месяц
            'max_credit_amount': 5000000,  # 5 млн максимальная сумма
            'min_credit_amount': 100000,  # 100 тыс минимальная сумма
            'rate_1_year': 0.12,  # 12% на 1 год
            'rate_over_1_year': 0.21,  # 21% свыше 1 года
            'min_age': 21,  # Минимальный возраст
            'max_age': 65,  # Максимальный возраст
            'min_credit_history': 1  # Минимум 1 кредитная операция
        }
        
        # Преимущества согласно требованиям
        self.benefits = {
            'no_collateral': True,  # Без залога
            'no_documents': True,  # Без справок
            'online_application': True,  # Оформление онлайн
            'early_repayment': True,  # Досрочное погашение без штрафов
            'partial_repayment': True,  # Частичное погашение
            'payment_deferral': True,  # Возможна отсрочка платежа
            'flexible_terms': True,  # Гибкие условия
            'quick_approval': True  # Быстрое одобрение
        }
    
    def analyze_client(self, client_code: str, days: int, db_manager) -> Dict[str, Any]:
        """
        Анализ соответствия клиента кредиту наличными
        Основан на исследованиях потребительского кредитования и финансового поведения
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
        if stability_score > 0.7:
            reasons.append('Высокая финансовая стабильность для кредитования')
        elif stability_score > 0.4:
            reasons.append('Достаточная финансовая стабильность')
        
        # 2. Анализ кредитного поведения (ключевой фактор - 30%)
        credit_score = self._analyze_credit_behavior(client_data)
        score += credit_score * 0.3
        if credit_score > 0.7:
            reasons.append('Опытный пользователь кредитных продуктов')
        elif credit_score > 0.4:
            reasons.append('Есть опыт кредитования')
        
        # 3. Анализ потребности в финансировании (важный фактор - 20%)
        need_score = self._analyze_financing_need(client_data)
        score += need_score * 0.2
        if need_score > 0.7:
            reasons.append('Высокая потребность в дополнительном финансировании')
        elif need_score > 0.4:
            reasons.append('Умеренная потребность в финансировании')
        
        # 4. Анализ статуса клиента (дополнительный фактор - 10%)
        status_score = self._analyze_status_suitability(status)
        score += status_score * 0.1
        if status_score > 0.7:
            reasons.append('Оптимальный статус для кредитования')
        elif status_score > 0.4:
            reasons.append('Подходящий статус для кредитования')
        
        # Нормализуем скор
        final_score = min(score, 1.0)
        
        # Дополнительные проверки на основе исследований
        if avg_balance < 100000:  # Менее 100 тыс
            final_score *= 0.2
            reasons.append('Недостаточная финансовая стабильность для кредита')
        elif avg_balance < 300000:  # Менее 300 тыс
            final_score *= 0.6
            reasons.append('Баланс ниже рекомендуемого для кредита наличными')
        
        # Проверка статуса клиента
        if status not in ['Премиальный клиент', 'Зарплатный клиент', 'Стандартный клиент', 'Студент']:
            final_score *= 0.3
            reasons.append('Статус не соответствует требованиям кредитования')
        
        # Бонус за высокую кредитную активность
        if hasattr(self, 'credit_activity_data') and self.credit_activity_data:
            credit_activity = self.credit_activity_data.get('credit_activity_ratio', 0)
            if credit_activity >= 0.3:  # 30%+ кредитных операций
                final_score = min(final_score * 1.2, 1.0)
                reasons.append('Бонус за высокую кредитную активность')
        
        expected_benefit = self.calculate_expected_benefit(client_data, final_score)
        
        return self.format_analysis_result(final_score, reasons, expected_benefit)
    
    def _analyze_financial_stability(self, avg_balance: float, status: str) -> float:
        """Анализ финансовой стабильности клиента"""
        # Базовый скор по балансу
        if avg_balance >= 2000000:  # 2+ млн - отлично
            return 1.0
        elif avg_balance >= 1000000:  # 1+ млн - хорошо
            return 0.8
        elif avg_balance >= 500000:  # 500+ тыс - удовлетворительно
            return 0.6
        elif avg_balance >= 300000:  # 300+ тыс - минимально
            return 0.4
        elif avg_balance >= 100000:  # 100+ тыс - слабо
            return 0.2
        else:  # Менее 100 тыс - плохо
            return 0.1
        
        # Бонус за статус клиента
        status_bonus = 0.0
        if status == 'Премиальный клиент':
            status_bonus = 0.2
        elif status == 'Зарплатный клиент':
            status_bonus = 0.1
        elif status == 'Стандартный клиент':
            status_bonus = 0.05
        
        return min(base_score + status_bonus, 1.0)
    
    def _analyze_credit_behavior(self, client_data: Dict) -> float:
        """Анализ кредитного поведения клиента по типам переводов"""
        transfers = client_data.get('transfers', [])
        if not transfers:
            return 0.0
        
        # Ищем кредитные операции по официальным типам переводов
        credit_types = ['loan_payment_out', 'cc_repayment_out', 'installment_payment_out']
        credit_count = 0
        total_transfers = len(transfers)
        
        for transfer in transfers:
            transfer_type = transfer.get('type', '')
            if transfer_type in credit_types:
                credit_count += 1
        
        # Сохраняем данные для анализа
        self.credit_activity_data = {
            'credit_count': credit_count,
            'total_transfers': total_transfers,
            'credit_activity_ratio': credit_count / total_transfers if total_transfers > 0 else 0
        }
        
        # Оцениваем опыт кредитования
        if credit_count >= 10:
            return 1.0
        elif credit_count >= 5:
            return 0.8
        elif credit_count >= 3:
            return 0.6
        elif credit_count >= 1:
            return 0.4
        else:
            return 0.1
    
    def _analyze_financing_need(self, client_data: Dict) -> float:
        """Анализ потребности в дополнительном финансировании"""
        transactions = client_data.get('transactions', [])
        transfers = client_data.get('transfers', [])
        
        if not transactions and not transfers:
            return 0.0
        
        # Анализируем траты по категориям, указывающим на потребность в финансировании
        high_value_categories = [
            'Медицина', 'Ремонт дома', 'Мебель', 'Авто', 'Путешествия',
            'Ювелирные украшения', 'Подарки', 'Спа и массаж'
        ]
        
        total_amount = 0
        high_value_amount = 0
        high_value_transactions = []
        
        for transaction in transactions:
            amount = float(transaction.get('amount', 0))
            category = transaction.get('category', '')
            
            total_amount += amount
            
            if category in high_value_categories:
                high_value_amount += amount
                high_value_transactions.append({
                    'amount': amount,
                    'category': category,
                    'date': transaction.get('date')
                })
        
        # Анализируем исходящие переводы (потребление средств)
        outgoing_amount = 0
        for transfer in transfers:
            if transfer.get('direction') == 'out':
                outgoing_amount += float(transfer.get('amount', 0))
        
        # Оцениваем потребность в финансировании
        if total_amount == 0:
            return 0.0
        
        # Доля высокоценных трат
        high_value_ratio = high_value_amount / total_amount
        
        # Соотношение трат к переводам (потребление vs поступления)
        consumption_ratio = total_amount / (outgoing_amount + 1) if outgoing_amount > 0 else 0
        
        # Комбинируем оценки
        high_value_score = min(high_value_ratio * 2, 1.0)  # До 50% высокоценных трат = 100% скора
        consumption_score = min(consumption_ratio * 0.5, 1.0)  # До 200% трат от переводов = 100% скора
        
        return (high_value_score + consumption_score) / 2
    
    def _analyze_status_suitability(self, status: str) -> float:
        """Анализ подходящего статуса для кредитования"""
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
        """Расчет ожидаемой выгоды от кредита наличными"""
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Базовая выгода как процент от баланса
        # Клиент получает доступ к дополнительным средствам
        base_benefit = avg_balance * 0.1  # 10% от баланса как доступный кредит
        
        # Дополнительная выгода от гибкости условий
        flexibility_benefit = avg_balance * 0.02  # 2% за гибкие условия
        
        # Бонус за быстрый доступ к средствам
        speed_benefit = avg_balance * 0.01  # 1% за скорость оформления
        
        total_benefit = (base_benefit + flexibility_benefit + speed_benefit) * score
        
        return total_benefit