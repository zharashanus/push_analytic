"""
Движок скоринга для оценки соответствия продуктов
"""

from typing import Dict, List, Any, Optional
import math


class ScoringEngine:
    """Движок для расчета скоринга и ожидаемой выгоды"""
    
    def __init__(self):
        self.weights = {
            'balance': 0.3,      # Вес баланса клиента
            'spending': 0.25,    # Вес трат
            'transfers': 0.2,    # Вес переводов
            'patterns': 0.15,    # Вес паттернов поведения
            'demographics': 0.1  # Вес демографических данных
        }
    
    def calculate_product_score(self, client_data: Dict, product_data: Dict, 
                              signals: List[Dict]) -> Dict[str, Any]:
        """
        Расчет скоринга продукта для клиента
        
        Args:
            client_data: Данные клиента
            product_data: Данные продукта
            signals: Список сигналов от аналитики
        
        Returns:
            Результат скоринга
        """
        score_components = {}
        total_score = 0.0
        
        # 1. Анализ баланса
        balance_score = self._calculate_balance_score(client_data, product_data)
        score_components['balance'] = balance_score
        total_score += balance_score * self.weights['balance']
        
        # 2. Анализ трат
        spending_score = self._calculate_spending_score(signals, product_data)
        score_components['spending'] = spending_score
        total_score += spending_score * self.weights['spending']
        
        # 3. Анализ переводов
        transfers_score = self._calculate_transfers_score(signals, product_data)
        score_components['transfers'] = transfers_score
        total_score += transfers_score * self.weights['transfers']
        
        # 4. Анализ паттернов
        patterns_score = self._calculate_patterns_score(signals, product_data)
        score_components['patterns'] = patterns_score
        total_score += patterns_score * self.weights['patterns']
        
        # 5. Демографические данные
        demographics_score = self._calculate_demographics_score(client_data, product_data)
        score_components['demographics'] = demographics_score
        total_score += demographics_score * self.weights['demographics']
        
        # Нормализуем скор до 0-1
        normalized_score = min(max(total_score, 0), 1)
        
        return {
            'total_score': normalized_score,
            'components': score_components,
            'weights': self.weights,
            'confidence': self._calculate_confidence(score_components)
        }
    
    def calculate_expected_benefit(self, client_data: Dict, product_data: Dict, 
                                 score: float) -> float:
        """
        Расчет ожидаемой выгоды от продукта
        
        Args:
            client_data: Данные клиента
            product_data: Данные продукта
            score: Скор продукта
        
        Returns:
            Ожидаемая выгода в тенге
        """
        avg_balance = client_data.get('avg_monthly_balance_kzt', 0)
        product_name = product_data.get('name', '')
        product_category = product_data.get('category', '')
        
        base_benefit = 0.0
        
        # Базовый расчет по категории продукта
        if product_category == 'cards':
            # Для карт - кешбэк и комиссии
            cashback_rate = product_data.get('cashback_rate', 0.02)  # 2% по умолчанию
            monthly_spending = avg_balance * 0.5  # Предполагаем траты 50% от баланса
            base_benefit = monthly_spending * cashback_rate * 12  # В год
            
        elif product_category == 'deposits':
            # Для депозитов - процентный доход
            interest_rate = product_data.get('interest_rate', 0.15)  # 15% по умолчанию
            deposit_amount = min(avg_balance * 0.8, product_data.get('max_amount', 10000000))
            base_benefit = deposit_amount * interest_rate
            
        elif product_category == 'credits':
            # Для кредитов - комиссия банка
            credit_limit = product_data.get('credit_limit', 1000000)
            commission_rate = product_data.get('commission_rate', 0.05)  # 5% комиссия
            base_benefit = credit_limit * commission_rate
            
        elif product_category == 'investments':
            # Для инвестиций - потенциальный доход
            investment_amount = min(avg_balance * 0.3, 5000000)  # До 5 млн
            expected_return = product_data.get('expected_return', 0.1)  # 10% доходность
            base_benefit = investment_amount * expected_return
        
        # Корректируем на скор
        adjusted_benefit = base_benefit * score
        
        return round(adjusted_benefit, 2)
    
    def _calculate_balance_score(self, client_data: Dict, product_data: Dict) -> float:
        """Расчет скора по балансу клиента"""
        avg_balance = client_data.get('avg_monthly_balance_kzt', 0)
        product_name = product_data.get('name', '')
        
        # Базовый скор по балансу
        if avg_balance < 100000:  # Менее 100 тыс
            base_score = 0.1
        elif avg_balance < 500000:  # 100-500 тыс
            base_score = 0.3
        elif avg_balance < 1000000:  # 500 тыс - 1 млн
            base_score = 0.6
        elif avg_balance < 3000000:  # 1-3 млн
            base_score = 0.8
        else:  # Более 3 млн
            base_score = 1.0
        
        # Корректировки для разных продуктов
        if 'премиальная' in product_name.lower():
            if avg_balance > 6000000:  # 6 млн для премиальной карты
                base_score = 1.0
            elif avg_balance > 3000000:  # 3 млн
                base_score = 0.7
            else:
                base_score = 0.3
        
        elif 'депозит' in product_name.lower():
            if avg_balance > 1000000:  # 1 млн для депозитов
                base_score = min(base_score + 0.2, 1.0)
        
        return base_score
    
    def _calculate_spending_score(self, signals: List[Dict], product_data: Dict) -> float:
        """Расчет скора по тратам клиента"""
        product_name = product_data.get('name', '')
        score = 0.5  # Базовый скор
        
        # Анализируем сигналы трат
        for signal in signals:
            signal_type = signal.get('signal', '')
            signal_strength = signal.get('strength', 0)
            
            if 'travel' in signal_type and 'путешествий' in product_name.lower():
                score += signal_strength * 0.3
            
            elif 'restaurant' in signal_type and 'кредитная' in product_name.lower():
                score += signal_strength * 0.2
            
            elif 'luxury' in signal_type and 'премиальная' in product_name.lower():
                score += signal_strength * 0.3
        
        return min(score, 1.0)
    
    def _calculate_transfers_score(self, signals: List[Dict], product_data: Dict) -> float:
        """Расчет скора по переводам клиента"""
        product_name = product_data.get('name', '')
        score = 0.5  # Базовый скор
        
        # Анализируем сигналы переводов
        for signal in signals:
            signal_type = signal.get('signal', '')
            signal_strength = signal.get('strength', 0)
            
            if 'currency' in signal_type and 'валют' in product_name.lower():
                score += signal_strength * 0.4
            
            elif 'salary' in signal_type and 'депозит' in product_name.lower():
                score += signal_strength * 0.2
        
        return min(score, 1.0)
    
    def _calculate_patterns_score(self, signals: List[Dict], product_data: Dict) -> float:
        """Расчет скора по паттернам поведения"""
        score = 0.5  # Базовый скор
        
        # Анализируем все сигналы
        for signal in signals:
            signal_strength = signal.get('strength', 0)
            score += signal_strength * 0.1  # Небольшой вклад каждого сигнала
        
        return min(score, 1.0)
    
    def _calculate_demographics_score(self, client_data: Dict, product_data: Dict) -> float:
        """Расчет скора по демографическим данным"""
        score = 0.5  # Базовый скор
        
        # Анализируем статус клиента
        status = client_data.get('status', '')
        if status == 'active':
            score += 0.2
        elif status == 'premium':
            score += 0.3
        
        # Анализируем город
        city = client_data.get('city', '')
        if city in ['Алматы', 'Нур-Султан', 'Шымкент']:  # Крупные города
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_confidence(self, score_components: Dict) -> float:
        """Расчет уверенности в скоре"""
        # Уверенность зависит от разброса компонентов
        scores = list(score_components.values())
        if not scores:
            return 0.0
        
        mean_score = sum(scores) / len(scores)
        variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
        std_dev = math.sqrt(variance)
        
        # Нормализуем до 0-1 (чем меньше разброс, тем выше уверенность)
        confidence = max(0, 1 - std_dev)
        return round(confidence, 3)
