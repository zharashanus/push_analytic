"""
Сценарий для обмена валют
Основан на исследованиях валютных операций и поведения клиентов
"""

from typing import Dict, List, Any
from .base_scenario_fixed import BaseProductScenario


class CurrencyExchangeScenario(BaseProductScenario):
    """Сценарий для обмена валют"""
    
    def __init__(self):
        super().__init__()
        self.product_name = "Обмен валют"
        self.category = "currency"
        self.description = "Выгодный курс в приложении, без комиссии, 24/7, авто-покупка по целевому курсу"
        self.target_audience = "Клиенты, часто меняющие валюту и следящие за курсом"
        
        # Условия основаны на исследованиях валютных операций
        self.conditions = {
            'min_balance': 100000,  # 100 тыс тенге (базовая активность)
            'min_fx_operations': 2,  # Минимум 2 валютные операции в месяц
            'min_fx_amount': 50000,  # 50 тыс тенге на валютные операции
            'currency_activity_threshold': 0.05  # 5% валютных операций от общих трат
        }
        
        # Преимущества согласно требованиям
        self.benefits = {
            'favorable_rate': True,  # Выгодный курс в приложении
            'no_commission': True,  # Без комиссии
            'available_24_7': True,  # 24/7 доступность
            'instant_operations': True,  # Моментальные операции
            'target_rate_alerts': True,  # Авто-покупка по целевому курсу
            'supported_currencies': ['USD', 'EUR', 'RUB', 'KZT']  # Поддерживаемые валюты
        }
    
    def analyze_client(self, client_code: str, days: int, db_manager) -> Dict[str, Any]:
        """
        Анализ соответствия клиента продукту обмена валют
        Основан на исследованиях валютных операций
        """
        client_data = self.get_client_data(client_code, days, db_manager)
        if not client_data:
            return self.format_analysis_result(0, ['Клиент не найден'], 0)
        
        reasons = []
        score = 0.0
        
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # 1. Анализ финансовой стабильности (основной критерий)
        stability_score = self._analyze_financial_stability(avg_balance)
        score += stability_score * 0.2
        if stability_score > 0.7:
            reasons.append('Высокая финансовая стабильность')
        elif stability_score > 0.4:
            reasons.append('Достаточная финансовая стабильность')
        
        # 2. Анализ валютных операций (ключевой фактор)
        fx_score = self._analyze_currency_operations(client_data)
        score += fx_score * 0.5
        if fx_score > 0.7:
            reasons.append('Активные валютные операции')
        elif fx_score > 0.4:
            reasons.append('Умеренные валютные операции')
        
        # 3. Анализ регулярности валютных операций
        regularity_score = self._analyze_currency_regularity(client_data)
        score += regularity_score * 0.2
        if regularity_score > 0.7:
            reasons.append('Регулярные валютные операции')
        elif regularity_score > 0.4:
            reasons.append('Периодические валютные операции')
        
        # 4. Анализ размера валютных операций
        amount_score = self._analyze_currency_amounts(client_data)
        score += amount_score * 0.1
        if amount_score > 0.6:
            reasons.append('Крупные валютные операции')
        
        # Нормализуем скор
        final_score = min(score, 1.0)
        
        # Дополнительные проверки
        if avg_balance < 50000:  # Менее 50 тыс
            final_score *= 0.3
            reasons.append('Недостаточный баланс для валютных операций')
        elif avg_balance < 100000:  # Менее 100 тыс
            final_score *= 0.6
            reasons.append('Баланс ниже рекомендуемого для валютных операций')
        
        # Бонус за высокую валютную активность
        if hasattr(self, 'fx_data') and self.fx_data:
            fx_ratio = self.fx_data.get('fx_ratio', 0)
            if fx_ratio >= 0.1:  # 10%+ валютных операций
                final_score = min(final_score * 1.2, 1.0)
                reasons.append('Бонус за высокую валютную активность')
        
        expected_benefit = self.calculate_expected_benefit(client_data, final_score)
        
        return self.format_analysis_result(final_score, reasons, expected_benefit)
    
    def _analyze_financial_stability(self, avg_balance: float) -> float:
        """Анализ финансовой стабильности клиента"""
        if avg_balance >= 1000000:  # 1+ млн - отлично
            return 1.0
        elif avg_balance >= 500000:  # 500+ тыс - хорошо
            return 0.8
        elif avg_balance >= 200000:  # 200+ тыс - удовлетворительно
            return 0.6
        elif avg_balance >= 100000:  # 100+ тыс - минимально
            return 0.4
        elif avg_balance >= 50000:  # 50+ тыс - слабо
            return 0.2
        else:  # Менее 50 тыс - плохо
            return 0.1
    
    def _analyze_currency_operations(self, client_data: Dict) -> float:
        """Анализ валютных операций по переводам"""
        transfers = client_data.get('transfers', [])
        if not transfers:
            return 0.0
        
        # Типы валютных операций из официальных источников
        fx_types = ['fx_buy', 'fx_sell', 'deposit_fx_topup_out', 'deposit_fx_withdraw_in']
        
        total_amount = 0
        fx_amount = 0
        fx_count = 0
        fx_transactions = []
        
        for transfer in transfers:
            amount = float(transfer.get('amount', 0))
            transfer_type = transfer.get('type', '')
            currency = transfer.get('currency', 'KZT')
            
            total_amount += amount
            
            # Проверяем валютные операции
            if transfer_type in fx_types or currency != 'KZT':
                fx_amount += amount
                fx_count += 1
                fx_transactions.append({
                    'amount': amount,
                    'type': transfer_type,
                    'currency': currency,
                    'date': transfer.get('date')
                })
        
        if total_amount == 0:
            return 0.0
        
        fx_ratio = fx_amount / total_amount
        
        # Сохраняем данные для уведомлений
        self.fx_data = {
            'total_amount': total_amount,
            'fx_amount': fx_amount,
            'fx_count': fx_count,
            'fx_ratio': fx_ratio,
            'fx_transactions': fx_transactions,
            'potential_savings': fx_amount * 0.01  # 1% экономия от выгодного курса
        }
        
        # Оцениваем по доле валютных операций
        if fx_ratio >= 0.2:  # 20%+ валютных операций
            return 1.0
        elif fx_ratio >= 0.1:  # 10-20%
            return 0.8
        elif fx_ratio >= 0.05:  # 5-10%
            return 0.6
        elif fx_ratio >= 0.02:  # 2-5%
            return 0.4
        else:
            return 0.2
    
    def _analyze_currency_regularity(self, client_data: Dict) -> float:
        """Анализ регулярности валютных операций"""
        transfers = client_data.get('transfers', [])
        if not transfers:
            return 0.0
        
        # Группируем валютные операции по месяцам
        monthly_fx = {}
        fx_types = ['fx_buy', 'fx_sell', 'deposit_fx_topup_out', 'deposit_fx_withdraw_in']
        
        for transfer in transfers:
            date = transfer.get('date')
            if not date:
                continue
            
            # Простая группировка по месяцу
            month_key = str(date)[:7]  # YYYY-MM
            
            transfer_type = transfer.get('type', '')
            currency = transfer.get('currency', 'KZT')
            
            # Проверяем на валютные операции
            is_fx = transfer_type in fx_types or currency != 'KZT'
            
            if is_fx:
                if month_key not in monthly_fx:
                    monthly_fx[month_key] = 0
                monthly_fx[month_key] += 1
        
        # Анализируем регулярность
        months_with_fx = len(monthly_fx)
        total_months = max(1, len(set(str(t.get('date', ''))[:7] for t in transfers)))
        
        regularity_ratio = months_with_fx / total_months
        
        if regularity_ratio >= 0.8:
            return 1.0
        elif regularity_ratio >= 0.6:
            return 0.8
        elif regularity_ratio >= 0.4:
            return 0.6
        elif regularity_ratio >= 0.2:
            return 0.4
        else:
            return 0.2
    
    def _analyze_currency_amounts(self, client_data: Dict) -> float:
        """Анализ размеров валютных операций"""
        transfers = client_data.get('transfers', [])
        if not transfers:
            return 0.0
        
        fx_types = ['fx_buy', 'fx_sell', 'deposit_fx_topup_out', 'deposit_fx_withdraw_in']
        fx_amounts = []
        
        for transfer in transfers:
            amount = float(transfer.get('amount', 0))
            transfer_type = transfer.get('type', '')
            currency = transfer.get('currency', 'KZT')
            
            # Проверяем валютные операции
            if transfer_type in fx_types or currency != 'KZT':
                fx_amounts.append(amount)
        
        if not fx_amounts:
            return 0.0
        
        # Оцениваем по среднему размеру операций
        avg_fx_amount = sum(fx_amounts) / len(fx_amounts)
        
        if avg_fx_amount >= 500000:  # 500+ тыс за операцию
            return 1.0
        elif avg_fx_amount >= 200000:  # 200+ тыс
            return 0.8
        elif avg_fx_amount >= 100000:  # 100+ тыс
            return 0.6
        elif avg_fx_amount >= 50000:  # 50+ тыс
            return 0.4
        else:
            return 0.2
    
    def calculate_expected_benefit(self, client_data: Dict, score: float) -> float:
        """Расчет ожидаемой выгоды от выгодного курса"""
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Базовая выгода от выгодного курса
        base_benefit = avg_balance * 0.005  # 0.5% экономия от курса
        
        # Дополнительная выгода от валютных операций
        if hasattr(self, 'fx_data') and self.fx_data:
            fx_benefit = self.fx_data.get('potential_savings', 0)
            base_benefit += fx_benefit
        
        return base_benefit * score