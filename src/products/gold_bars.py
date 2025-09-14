"""
Сценарий для золотых слитков
Основан на авторитетных исследованиях инвестиций в драгоценные металлы и диверсификации портфеля
"""

from typing import Dict, List, Any
from .base_scenario_fixed import BaseProductScenario


class GoldBarsScenario(BaseProductScenario):
    """Сценарий для золотых слитков"""
    
    def __init__(self):
        super().__init__()
        self.product_name = "Золотые слитки"
        self.category = "investments"
        self.description = "Слитки 999,9 пробы разных весов, покупка/продажа в отделениях и приложении, хранение в сейфовых ячейках банка"
        self.target_audience = "Клиенты для диверсификации и долгосрочного сохранения стоимости"
        
        # Условия основаны на исследованиях инвестиций в драгоценные металлы
        self.conditions = {
            'min_balance': 1000000,  # 1 млн тенге (базовый уровень для золота)
            'purity': 999.9,  # 999,9 проба (высшая чистота)
            'weights_available': [5, 10, 20, 50, 100],  # Доступные веса в граммах
            'purchase_methods': ['отделения', 'приложение'],  # Способы покупки
            'storage_available': True,  # Хранение в сейфовых ячейках
            'min_age': 18,  # Минимальный возраст
            'max_age': 70,  # Максимальный возраст
            'nds_rate': 0.12,  # НДС 12% при покупке
            'storage_cost': 36000  # Стоимость хранения в год (тенге)
        }
        
        # Преимущества согласно требованиям и исследованиям
        self.benefits = {
            'purity': 999.9,  # 999,9 проба (высшая чистота)
            'multiple_weights': True,  # Разные веса слитков
            'bank_storage': True,  # Хранение в сейфовых ячейках банка
            'long_term_preservation': True,  # Долгосрочное сохранение стоимости
            'diversification': True,  # Диверсификация портфеля
            'inflation_protection': True,  # Защита от инфляции
            'high_liquidity': True,  # Высокая ликвидность
            'app_purchase': True  # Покупка через приложение
        }
    
    def analyze_client(self, client_code: str, days: int, db_manager) -> Dict[str, Any]:
        """
        Анализ соответствия клиента золотым слиткам
        Основан на исследованиях инвестиций в драгоценные металлы и диверсификации портфеля
        """
        client_data = self.get_client_data(client_code, days, db_manager)
        if not client_data:
            return self.format_analysis_result(0, ['Клиент не найден'], 0)
        
        reasons = []
        score = 0.0
        
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        status = client_info.get('status', '')
        
        # 1. Анализ финансовой готовности (основной критерий - 40%)
        readiness_score = self._analyze_financial_readiness(avg_balance, status)
        score += readiness_score * 0.4
        if readiness_score > 0.8:
            reasons.append('Высокая финансовая готовность для инвестиций в золото')
        elif readiness_score > 0.5:
            reasons.append('Достаточная финансовая готовность')
        
        # 2. Анализ диверсификационных потребностей (ключевой фактор - 30%)
        diversification_score = self._analyze_diversification_needs(client_data)
        score += diversification_score * 0.3
        if diversification_score > 0.7:
            reasons.append('Потребность в диверсификации портфеля')
        elif diversification_score > 0.4:
            reasons.append('Умеренная потребность в диверсификации')
        
        # 3. Анализ долгосрочного инвестиционного поведения (важный фактор - 20%)
        longterm_score = self._analyze_longterm_behavior(client_data)
        score += longterm_score * 0.2
        if longterm_score > 0.6:
            reasons.append('Склонность к долгосрочному сохранению стоимости')
        elif longterm_score > 0.3:
            reasons.append('Умеренная склонность к долгосрочным инвестициям')
        
        # 4. Анализ статуса клиента (дополнительный фактор - 10%)
        status_score = self._analyze_status_suitability(status)
        score += status_score * 0.1
        if status_score > 0.7:
            reasons.append('Оптимальный статус для инвестиций в золото')
        elif status_score > 0.4:
            reasons.append('Подходящий статус для золотых слитков')
        
        # Нормализуем скор
        final_score = min(score, 1.0)
        
        # Дополнительные проверки на основе исследований
        if avg_balance < 500000:  # Менее 500 тыс
            final_score *= 0.2
            reasons.append('Недостаточные средства для инвестиций в золото')
        elif avg_balance < 1000000:  # Менее 1 млн
            final_score *= 0.6
            reasons.append('Минимальные средства для золотых слитков')
        
        # Проверка статуса клиента
        if status not in ['Премиальный клиент', 'Зарплатный клиент', 'Стандартный клиент', 'Студент']:
            final_score *= 0.3
            reasons.append('Статус не соответствует требованиям для золотых слитков')
        
        # Бонус за высокую диверсификационную активность
        if hasattr(self, 'diversification_data') and self.diversification_data:
            diversification_ratio = self.diversification_data.get('diversification_ratio', 0)
            if diversification_ratio >= 0.3:  # 30%+ диверсификационных операций
                final_score = min(final_score * 1.15, 1.0)
                reasons.append('Бонус за высокую диверсификационную активность')
        
        expected_benefit = self.calculate_expected_benefit(client_data, final_score)
        
        return self.format_analysis_result(final_score, reasons, expected_benefit)
    
    def _analyze_financial_readiness(self, avg_balance: float, status: str) -> float:
        """Анализ финансовой готовности для инвестиций в золото"""
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
            status_bonus = 0.15
        elif status == 'Стандартный клиент':
            status_bonus = 0.1
        elif status == 'Студент':
            status_bonus = 0.05
        
        return min(base_score + status_bonus, 1.0)
    
    def _analyze_diversification_needs(self, client_data: Dict) -> float:
        """Анализ потребности в диверсификации портфеля"""
        transfers = client_data.get('transfers', [])
        
        # Официальные типы операций, указывающие на потребность в диверсификации
        diversification_types = ['invest_in', 'invest_out', 'fx_buy', 'fx_sell', 'deposit_topup_out', 'deposit_fx_topup_out']
        
        diversification_operations = 0
        total_transfers = len(transfers)
        
        for transfer in transfers:
            transfer_type = transfer.get('type', '')
            if transfer_type in diversification_types:
                diversification_operations += 1
        
        if total_transfers == 0:
            return 0.0
        
        diversification_ratio = diversification_operations / total_transfers
        
        # Сохраняем данные для анализа
        self.diversification_data = {
            'diversification_operations': diversification_operations,
            'total_transfers': total_transfers,
            'diversification_ratio': diversification_ratio
        }
        
        # Оцениваем потребность в диверсификации
        if diversification_ratio >= 0.4:  # 40%+ диверсификационных операций
            return 1.0
        elif diversification_ratio >= 0.3:  # 30-40%
            return 0.8
        elif diversification_ratio >= 0.2:  # 20-30%
            return 0.6
        elif diversification_ratio >= 0.1:  # 10-20%
            return 0.4
        else:
            return 0.1
    
    def _analyze_longterm_behavior(self, client_data: Dict) -> float:
        """Анализ долгосрочного инвестиционного поведения"""
        transfers = client_data.get('transfers', [])
        
        # Официальные типы операций, указывающие на долгосрочное поведение
        longterm_types = ['deposit_topup_out', 'deposit_fx_topup_out', 'invest_in', 'gold_buy_out']
        
        longterm_operations = 0
        for transfer in transfers:
            transfer_type = transfer.get('type', '')
            if transfer_type in longterm_types:
                longterm_operations += 1
        
        # Оцениваем по количеству долгосрочных операций
        if longterm_operations >= 5:
            return 1.0
        elif longterm_operations >= 3:
            return 0.8
        elif longterm_operations >= 2:
            return 0.6
        elif longterm_operations >= 1:
            return 0.4
        else:
            return 0.1
    
    def _analyze_status_suitability(self, status: str) -> float:
        """Анализ подходящего статуса для инвестиций в золото"""
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
        """Расчет ожидаемой выгоды от инвестиций в золотые слитки"""
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Базовая выгода от инвестиций в золото (консервативная оценка)
        base_benefit = avg_balance * 0.03  # 3% потенциальный доход от золота
        
        # Дополнительная выгода от диверсификации
        diversification_benefit = avg_balance * 0.01  # 1% за диверсификацию
        
        # Бонус за долгосрочное сохранение стоимости
        preservation_bonus = avg_balance * 0.005  # 0.5% за сохранение стоимости
        
        total_benefit = (base_benefit + diversification_benefit + preservation_bonus) * score
        
        return total_benefit
