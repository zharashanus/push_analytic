"""
Сценарий для кредитной карты
Основан на авторитетных исследованиях потребительского поведения и рынка кредитных карт
"""

from typing import Dict, List, Any
from .base_scenario_fixed import BaseProductScenario


class CreditCardScenario(BaseProductScenario):
    """Сценарий для кредитной карты"""
    
    def __init__(self):
        super().__init__()
        self.product_name = "Кредитная карта"
        self.category = "cards"
        self.description = "До 10% кешбэк в любимых категориях, кредитный лимит до 2 млн, рассрочка 3-24 мес"
        self.target_audience = "Клиенты, оптимизирующие траты под категории и пользующиеся рассрочкой"
        
        # Условия основаны на исследованиях рынка кредитных карт
        self.conditions = {
            'min_balance': 200000,  # 200 тыс тенге (финансовая стабильность)
            'min_monthly_spending': 100000,  # 100 тыс трат в месяц
            'credit_limit': 2000000,  # 2 млн лимит
            'grace_period': 60,  # 2 месяца без переплаты
            'min_online_spending': 0.15,  # 15% трат на онлайн услуги
            'favorite_categories_count': 3  # 3 любимые категории
        }
        
        # Преимущества согласно требованиям и исследованиям
        self.benefits = {
            'max_cashback': 0.10,  # 10% кешбэк в любимых категориях
            'online_cashback': 0.10,  # 10% на онлайн услуги
            'installment_periods': [3, 6, 12, 18, 24],  # Рассрочка 3-24 мес
            'favorite_categories': 3,  # 3 любимые категории
            'grace_period_days': 60,  # 2 месяца без переплаты
            'cashback_limit': 100000  # 100 тыс лимит кешбэка
        }
    
    def analyze_client(self, client_code: str, days: int, db_manager) -> Dict[str, Any]:
        """
        Анализ соответствия клиента кредитной карте
        Основан на исследованиях потребительского поведения и рынка кредитных карт
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
        score += stability_score * 0.25
        if stability_score > 0.7:
            reasons.append('Высокая финансовая стабильность')
        elif stability_score > 0.4:
            reasons.append('Достаточная финансовая стабильность')
        
        # 2. Анализ трат по категориям (ключевой фактор по исследованиям)
        category_score = self._analyze_spending_categories(client_data)
        score += category_score * 0.35
        if category_score > 0.7:
            reasons.append('Активные траты в популярных категориях для кешбэка')
        elif category_score > 0.4:
            reasons.append('Умеренные траты в различных категориях')
        
        # 3. Анализ онлайн трат (важный фактор по исследованиям)
        online_score = self._analyze_online_spending(client_data)
        score += online_score * 0.2
        if online_score > 0.6:
            reasons.append('Высокие траты на онлайн услуги (игры, доставка, кино)')
        elif online_score > 0.3:
            reasons.append('Умеренные онлайн траты')
        
        # 4. Анализ регулярности трат (паттерн поведения)
        regularity_score = self._analyze_spending_regularity(client_data)
        score += regularity_score * 0.15
        if regularity_score > 0.7:
            reasons.append('Регулярные траты - идеально для кешбэка')
        elif regularity_score > 0.4:
            reasons.append('Стабильные траты')
        
        # 5. Анализ кредитного поведения
        credit_score = self._analyze_credit_behavior(client_data)
        score += credit_score * 0.05
        if credit_score > 0.6:
            reasons.append('Опыт использования кредитных средств')
        
        # Нормализуем скор
        final_score = min(score, 1.0)
        
        # Дополнительные проверки на основе исследований
        if avg_balance < 100000:  # Менее 100 тыс
            final_score *= 0.3
            reasons.append('Недостаточная финансовая стабильность для кредита')
        elif avg_balance < 200000:  # Менее 200 тыс
            final_score *= 0.6
            reasons.append('Баланс ниже рекомендуемого для кредитной карты')
        
        # Бонус за высокие онлайн траты (исследования показали важность)
        if hasattr(self, 'online_spending_data') and self.online_spending_data:
            online_ratio = self.online_spending_data.get('online_ratio', 0)
            if online_ratio >= 0.3:  # 30%+ онлайн трат
                final_score = min(final_score * 1.15, 1.0)
                reasons.append('Бонус за высокие онлайн траты')
        
        expected_benefit = self.calculate_expected_benefit(client_data, final_score)
        
        return self.format_analysis_result(final_score, reasons, expected_benefit)
    
    def _analyze_financial_stability(self, avg_balance: float) -> float:
        """Анализ финансовой стабильности клиента"""
        if avg_balance >= 1000000:  # 1+ млн - отлично
            return 1.0
        elif avg_balance >= 500000:  # 500+ тыс - хорошо
            return 0.8
        elif avg_balance >= 300000:  # 300+ тыс - удовлетворительно
            return 0.6
        elif avg_balance >= 200000:  # 200+ тыс - минимально
            return 0.4
        elif avg_balance >= 100000:  # 100+ тыс - слабо
            return 0.2
        else:  # Менее 100 тыс - плохо
            return 0.1
    
    def _analyze_credit_behavior(self, client_data: Dict) -> float:
        """Анализ кредитного поведения клиента по типам переводов"""
        transfers = client_data.get('transfers', [])
        if not transfers:
            return 0.0
        
        # Ищем кредитные операции по официальным типам переводов
        credit_types = ['loan_payment_out', 'cc_repayment_out', 'installment_payment_out']
        credit_count = 0
        
        for transfer in transfers:
            transfer_type = transfer.get('type', '')
            
            if transfer_type in credit_types:
                credit_count += 1
        
        # Оцениваем опыт кредитования
        if credit_count >= 5:
            return 1.0
        elif credit_count >= 3:
            return 0.7
        elif credit_count >= 1:
            return 0.4
        else:
            return 0.1
    
    def _analyze_spending_categories(self, client_data: Dict) -> float:
        """Анализ трат по категориям для кешбэка"""
        transactions = client_data.get('transactions', [])
        if not transactions:
            return 0.0
        
        # Популярные категории для кешбэка (только официальные категории)
        popular_categories = [
            'Кафе и рестораны', 'Продукты питания', 'Одежда и обувь',
            'Развлечения', 'Кино', 'Играем дома', 'Смотрим дома',
            'Косметика и Парфюмерия', 'Спорт', 'Медицина', 'Авто', 'АЗС',
            'Такси', 'Отели', 'Путешествия', 'Подарки', 'Ювелирные украшения'
        ]
        
        total_amount = 0
        popular_amount = 0
        category_counts = {}
        category_amounts = {}
        
        for transaction in transactions:
            amount = float(transaction.get('amount', 0))
            category = transaction.get('category', '')
            
            total_amount += amount
            
            # Проверяем только по официальным категориям
            if category in popular_categories:
                popular_amount += amount
                category_counts[category] = category_counts.get(category, 0) + 1
                category_amounts[category] = category_amounts.get(category, 0) + amount
        
        if total_amount == 0:
            return 0.0
        
        # Оцениваем по доле популярных трат
        popular_ratio = popular_amount / total_amount
        
        # Оцениваем разнообразие категорий (важно для выбора 3 любимых)
        category_diversity = len(category_counts) / len(popular_categories)
        
        # Оцениваем концентрацию трат в топ-3 категориях
        top_3_amount = sum(sorted(category_amounts.values(), reverse=True)[:3])
        concentration_ratio = top_3_amount / popular_amount if popular_amount > 0 else 0
        
        # Комбинируем оценки
        ratio_score = min(popular_ratio * 2, 1.0)  # До 50% трат = 100% скора
        diversity_score = min(category_diversity * 2, 1.0)  # До 50% категорий = 100% скора
        concentration_score = min(concentration_ratio * 1.5, 1.0)  # До 67% в топ-3 = 100% скора
        
        return (ratio_score + diversity_score + concentration_score) / 3
    
    def _analyze_spending_regularity(self, client_data: Dict) -> float:
        """Анализ регулярности трат"""
        transactions = client_data.get('transactions', [])
        if not transactions:
            return 0.0
        
        # Группируем по неделям
        weekly_spending = {}
        for transaction in transactions:
            date = transaction.get('date')
            if not date:
                continue
            
            # Простая группировка по неделе
            week_key = str(date)[:10]  # YYYY-MM-DD, упрощенно
            
            amount = float(transaction.get('amount', 0))
            if week_key not in weekly_spending:
                weekly_spending[week_key] = 0
            weekly_spending[week_key] += amount
        
        if not weekly_spending:
            return 0.0
        
        # Анализируем регулярность
        spending_amounts = list(weekly_spending.values())
        avg_weekly = sum(spending_amounts) / len(spending_amounts)
        
        # Считаем недели с тратами выше среднего
        active_weeks = sum(1 for amount in spending_amounts if amount >= avg_weekly * 0.5)
        regularity_ratio = active_weeks / len(spending_amounts)
        
        if regularity_ratio >= 0.8:
            return 1.0
        elif regularity_ratio >= 0.6:
            return 0.7
        elif regularity_ratio >= 0.4:
            return 0.5
        else:
            return 0.2
    
    def _analyze_online_spending(self, client_data: Dict) -> float:
        """Анализ онлайн трат (игры, доставка, кино)"""
        transactions = client_data.get('transactions', [])
        if not transactions:
            return 0.0
        
        # Онлайн категории (только официальные категории)
        online_categories = [
            'Кино', 'Играем дома', 'Смотрим дома'
        ]
        
        total_amount = 0
        online_amount = 0
        online_transactions = []
        
        for transaction in transactions:
            amount = float(transaction.get('amount', 0))
            category = transaction.get('category', '')
            
            total_amount += amount
            
            # Проверяем только по официальным категориям
            if category in online_categories:
                online_amount += amount
                online_transactions.append({
                    'amount': amount,
                    'category': category,
                    'date': transaction.get('date')
                })
        
        if total_amount == 0:
            return 0.0
        
        online_ratio = online_amount / total_amount
        
        # Сохраняем данные для уведомлений
        self.online_spending_data = {
            'total_amount': total_amount,
            'online_amount': online_amount,
            'online_ratio': online_ratio,
            'online_transactions': online_transactions,
            'potential_cashback': online_amount * self.benefits['online_cashback']
        }
        
        # Оцениваем по доле онлайн трат
        if online_ratio >= 0.3:  # 30%+ онлайн трат
            return 1.0
        elif online_ratio >= 0.2:  # 20-30%
            return 0.8
        elif online_ratio >= 0.15:  # 15-20%
            return 0.6
        elif online_ratio >= 0.1:  # 10-15%
            return 0.4
        else:
            return 0.2
    
    def calculate_expected_benefit(self, client_data: Dict, score: float) -> float:
        """Расчет ожидаемой выгоды с учетом кешбэка и рассрочки"""
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Базовая выгода от кешбэка в любимых категориях
        base_benefit = avg_balance * 0.05  # 5% средний кешбэк
        
        # Дополнительная выгода от онлайн трат
        if hasattr(self, 'online_spending_data') and self.online_spending_data:
            online_benefit = self.online_spending_data.get('potential_cashback', 0)
            base_benefit += online_benefit
        
        # Бонус за рассрочку (экономия на процентах)
        installment_bonus = avg_balance * 0.02  # 2% экономия от рассрочки
        base_benefit += installment_bonus
        
        return base_benefit * score
