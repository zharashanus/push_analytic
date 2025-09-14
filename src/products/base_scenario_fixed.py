"""
Базовый класс для сценариев продуктов (исправленная версия под реальную БД)
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseProductScenario(ABC):
    """Базовый класс для всех сценариев продуктов"""
    
    def __init__(self):
        self.product_name = ""
        self.category = ""
        self.description = ""
        self.target_audience = ""
        self.conditions = {}
        self.benefits = {}
    
    @abstractmethod
    def analyze_client(self, client_code: str, days: int, db_manager) -> Dict[str, Any]:
        """
        Анализ соответствия клиента продукту
        
        Args:
            client_code: Код клиента
            days: Период анализа в днях
            db_manager: Менеджер базы данных
        
        Returns:
            Результат анализа с скором и причинами
        """
        pass
    
    def get_client_data(self, client_code: str, days: int, db_manager) -> Dict[str, Any]:
        """Получить данные клиента для анализа"""
        # Получаем информацию о клиенте
        client_info = db_manager.get_client_by_code(client_code)
        if not client_info:
            return {}
        
        # Получаем транзакции
        transactions = self._get_transactions_period(client_code, days, db_manager)
        
        # Получаем переводы
        transfers = self._get_transfers_period(client_code, days, db_manager)
        
        return {
            'client_info': client_info,
            'transactions': transactions,
            'transfers': transfers,
            'period_days': days
        }
    
    def _get_transactions_period(self, client_code: str, days: int, db_manager) -> List[Dict]:
        """Получить транзакции за период"""
        query = """
        SELECT t.*, c.name as client_name
        FROM "Transactions" t
        JOIN "Clients" c ON t.client_code = c.client_code
        WHERE t.client_code = %s
        AND t.date >= CURRENT_DATE - INTERVAL '%s days'
        ORDER BY t.date DESC
        """
        
        try:
            result = db_manager.execute_query(query, (client_code, days))
            return result if result else []
        except Exception as e:
            print(f"Ошибка получения транзакций: {e}")
            return []
    
    def _get_transfers_period(self, client_code: str, days: int, db_manager) -> List[Dict]:
        """Получить переводы за период"""
        query = """
        SELECT tr.*, c.name as client_name
        FROM "Transfers" tr
        JOIN "Clients" c ON tr.client_code = c.client_code
        WHERE tr.client_code = %s
        AND tr.date >= CURRENT_DATE - INTERVAL '%s days'
        ORDER BY tr.date DESC
        """
        
        try:
            result = db_manager.execute_query(query, (client_code, days))
            return result if result else []
        except Exception as e:
            print(f"Ошибка получения переводов: {e}")
            return []
    
    def calculate_basic_score(self, client_data: Dict) -> float:
        """Базовый расчет скора по балансу клиента"""
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        if avg_balance < 100000:  # Менее 100 тыс
            return 0.1
        elif avg_balance < 500000:  # 100-500 тыс
            return 0.3
        elif avg_balance < 1000000:  # 500 тыс - 1 млн
            return 0.6
        elif avg_balance < 3000000:  # 1-3 млн
            return 0.8
        else:  # Более 3 млн
            return 1.0
    
    def calculate_expected_benefit(self, client_data: Dict, score: float) -> float:
        """Расчет ожидаемой выгоды от продукта"""
        client_info = client_data.get('client_info', {})
        avg_balance = float(client_info.get('avg_monthly_balance_KZT', 0))
        
        # Базовая выгода зависит от баланса и скора
        base_benefit = avg_balance * 0.02 * score  # 2% от баланса, скорректированная на скор
        
        return round(base_benefit, 2)
    
    def format_analysis_result(self, score: float, reasons: List[str], expected_benefit: float) -> Dict[str, Any]:
        """Форматирование результата анализа"""
        return {
            'score': score,
            'reasons': reasons,
            'expected_benefit': expected_benefit,
            'match_score': {
                'score': score,
                'reasons': reasons
            }
        }
    
    def analyze_spending_patterns(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Анализ паттернов трат"""
        if not transactions:
            return {}
        
        # Группируем по категориям
        category_spending = {}
        total_amount = 0
        
        for transaction in transactions:
            amount = float(transaction.get('amount', 0))
            category = transaction.get('category', '')
            
            total_amount += amount
            
            if category not in category_spending:
                category_spending[category] = 0
            category_spending[category] += amount
        
        # Сортируем по сумме трат
        top_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_amount': total_amount,
            'category_spending': category_spending,
            'top_categories': top_categories[:5],  # Топ-5 категорий
            'category_count': len(category_spending)
        }
    
    def analyze_transfer_patterns(self, transfers: List[Dict]) -> Dict[str, Any]:
        """Анализ паттернов переводов"""
        if not transfers:
            return {}
        
        # Группируем по типам
        type_transfers = {}
        total_in = 0
        total_out = 0
        
        for transfer in transfers:
            amount = float(transfer.get('amount', 0))
            transfer_type = transfer.get('type', '')
            direction = transfer.get('direction', '')
            
            if direction == 'in':
                total_in += amount
            elif direction == 'out':
                total_out += amount
            
            if transfer_type not in type_transfers:
                type_transfers[transfer_type] = {'in': 0, 'out': 0}
            type_transfers[transfer_type][direction] += amount
        
        return {
            'total_in': total_in,
            'total_out': total_out,
            'net_flow': total_in - total_out,
            'type_transfers': type_transfers,
            'transfer_count': len(transfers)
        }
    
    def get_client_demographics(self, client_info: Dict) -> Dict[str, Any]:
        """Получить демографические данные клиента"""
        return {
            'status': client_info.get('status', ''),
            'city': client_info.get('city', ''),
            'avg_balance': client_info.get('avg_monthly_balance_KZT', 0)
        }
