"""
Сценарий для карты путешествий (исправленная версия под реальную БД)
"""

from typing import Dict, List, Any
from .base_scenario_fixed import BaseProductScenario


class TravelCardScenario(BaseProductScenario):
    """Сценарий для карты путешествий"""
    
    def __init__(self):
        super().__init__()
        self.product_name = "Карта для путешествий"
        self.category = "cards"
        self.description = "4% кешбэк на путешествия, такси, поезда, самолеты"
        self.target_audience = "Клиенты 20-39 лет с активными тратами на путешествия"
        
        # Правила основаны на исследованиях:
        # 1. Cyberleninka.ru: программы лояльности и кешбэк - ключевые драйверы
        # 2. RIA.ru: 63% пользователей карт в возрасте 20-39 лет
        # 3. Antrop.net: важность финансовой грамотности и контроля расходов
        self.conditions = {
            'min_balance': 100000,  # 100 тыс тенге (базовый порог)
            'travel_spending_threshold': 0.12,  # 12% трат на путешествия
            'min_travel_amount': 50000,  # 50 тыс тенге/месяц на путешествия
            'age_range': (20, 39),  # Основная целевая аудитория по исследованиям
            'regularity_threshold': 0.4  # 40% месяцев с поездками
        }
        self.benefits = {
            'cashback_rate': 0.04,  # 4% кешбэк
            'categories': ['такси', 'отели', 'путешествия'],  # Только реальные категории из БД
            'bonus_features': ['привилегии Visa Signature', 'скидки на отели', 'бесплатная страховка']
        }
    
    def analyze_client(self, client_code: str, days: int, db_manager) -> Dict[str, Any]:
        """
        Анализ соответствия клиента карте путешествий
        Основан на исследованиях потребительского поведения
        """
        client_data = self.get_client_data(client_code, days, db_manager)
        if not client_data:
            return self.format_analysis_result(0, ['Клиент не найден'], 0)
        
        reasons = []
        score = 0.0
        
        # 1. Анализ статуса клиента (вместо возраста)
        status_score = self._analyze_client_status(client_data)
        score += status_score * 0.2
        if status_score > 0.7:
            reasons.append('Подходящий статус клиента для карты путешествий')
        
        # 2. Базовый скор по балансу (финансовая стабильность)
        base_score = self.calculate_basic_score(client_data)
        score += base_score * 0.25
        if base_score > 0.5:
            reasons.append('Достаточный баланс для карты')
        
        # 3. Анализ трат на путешествия (ключевой фактор по исследованиям)
        travel_score = self._analyze_travel_spending(client_data)
        score += travel_score * 0.4
        if travel_score > 0.3:
            reasons.append('Активные траты на путешествия и транспорт')
        
        # 4. Анализ регулярности поездок (паттерн поведения)
        regularity_score = self._analyze_travel_regularity(client_data)
        score += regularity_score * 0.15
        if regularity_score > 0.5:
            reasons.append('Регулярные поездки')
        
        # Нормализуем скор
        final_score = min(score, 1.0)
        
        # Дополнительные проверки на основе исследований
        if travel_score < 0.1:
            final_score *= 0.3
            reasons.append('Низкая активность в путешествиях')
        
        # Бонус за высокие траты (исследование показало важность кешбэка)
        if hasattr(self, 'travel_data') and self.travel_data:
            monthly_travel = self.travel_data.get('travel_amount', 0)
            if monthly_travel > 100000:  # 100+ тыс тенге/месяц
                final_score = min(final_score * 1.2, 1.0)
                reasons.append('Высокие траты на путешествия')
        
        expected_benefit = self.calculate_expected_benefit(client_data, final_score)
        
        return self.format_analysis_result(final_score, reasons, expected_benefit)
    
    def _analyze_age_group(self, client_data: Dict) -> float:
        """Анализ возрастной группы клиента (удален - поле age не существует)"""
        # Поле age не существует в официальных источниках данных
        # Возвращаем нейтральный скор для всех клиентов
        return 0.5
    
    def _analyze_client_status(self, client_data: Dict) -> float:
        """Анализ статуса клиента"""
        client_info = client_data.get('client_info', {})
        status = client_info.get('status', '').lower()
        
        if 'премиальный' in status:
            return 1.0
        elif 'зарплатный' in status:
            return 0.8
        elif 'стандартный' in status:
            return 0.6
        elif 'студент' in status:
            return 0.4
        else:
            return 0.5
    
    def _analyze_travel_spending(self, client_data: Dict) -> float:
        """Анализ трат на путешествия (исправленная версия под реальную БД)"""
        transactions = client_data.get('transactions', [])
        if not transactions:
            return 0.0
        
        # Только реальные категории из БД
        travel_categories = ['Такси', 'Отели', 'Путешествия']
        
        total_amount = 0
        travel_amount = 0
        travel_transactions = []
        
        for transaction in transactions:
            amount = float(transaction.get('amount', 0))
            category = transaction.get('category', '')
            
            total_amount += amount
            
            # Проверяем только категорию (без описания)
            is_travel = category in travel_categories
            
            if is_travel:
                travel_amount += amount
                travel_transactions.append({
                    'amount': amount,
                    'category': category,
                    'date': transaction.get('date')
                })
        
        if total_amount == 0:
            return 0.0
        
        travel_ratio = travel_amount / total_amount
        threshold = self.conditions['travel_spending_threshold']
        min_amount = self.conditions['min_travel_amount']
        
        # Сохраняем данные для уведомлений
        self.travel_data = {
            'total_amount': total_amount,
            'travel_amount': travel_amount,
            'travel_ratio': travel_ratio,
            'travel_transactions': travel_transactions,
            'potential_cashback': travel_amount * self.benefits['cashback_rate']
        }
        
        # Комбинированная оценка: и процент, и абсолютная сумма
        # Исследования показали важность как относительных, так и абсолютных трат
        if travel_ratio >= threshold and travel_amount >= min_amount:
            return 1.0
        elif travel_ratio >= threshold * 0.8 and travel_amount >= min_amount * 0.8:
            return 0.8
        elif travel_ratio >= threshold * 0.5 or travel_amount >= min_amount * 0.5:
            return 0.6
        elif travel_ratio >= threshold * 0.2 or travel_amount >= min_amount * 0.2:
            return 0.3
        else:
            return 0.1
    
    def _analyze_travel_regularity(self, client_data: Dict) -> float:
        """Анализ регулярности поездок (исправленная версия)"""
        transactions = client_data.get('transactions', [])
        if not transactions:
            return 0.0
        
        # Группируем по месяцам
        monthly_travel = {}
        travel_categories = ['Такси', 'Отели', 'Путешествия']
        
        for transaction in transactions:
            date = transaction.get('date')
            if not date:
                continue
            
            # Простая группировка по месяцу
            month_key = str(date)[:7]  # YYYY-MM
            
            category = transaction.get('category', '')
            
            # Проверяем на путешествия (только категории)
            is_travel = category in travel_categories
            
            if is_travel:
                if month_key not in monthly_travel:
                    monthly_travel[month_key] = 0
                monthly_travel[month_key] += 1
        
        # Анализируем регулярность
        months_with_travel = len(monthly_travel)
        total_months = max(1, len(set(str(t.get('date', ''))[:7] for t in transactions)))
        
        regularity_ratio = months_with_travel / total_months
        
        if regularity_ratio >= 0.8:
            return 1.0
        elif regularity_ratio >= 0.5:
            return 0.7
        elif regularity_ratio >= 0.3:
            return 0.4
        else:
            return 0.1
