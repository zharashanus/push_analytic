"""
Детектор паттернов поведения клиента
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd


class PatternDetector:
    """Детектор паттернов поведения для генерации сигналов"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def detect_client_patterns(self, client_code: str, days: int = 90) -> Dict[str, Any]:
        """
        Детекция всех паттернов поведения клиента
        
        Args:
            client_code: Код клиента
            days: Период анализа в днях
        
        Returns:
            Словарь с обнаруженными паттернами
        """
        # Получаем данные клиента
        client_info = self.db.get_client_by_code(client_code)
        if not client_info:
            return {}
        
        # Получаем транзакции и переводы
        transactions = self._get_transactions_period(client_code, days)
        transfers = self._get_transfers_period(client_code, days)
        
        patterns = {
            'client_code': client_code,
            'client_info': client_info,
            'spending_patterns': self._detect_spending_patterns(transactions),
            'financial_behavior': self._detect_financial_behavior(transactions, transfers),
            'lifestyle_signals': self._detect_lifestyle_signals(transactions),
            'investment_readiness': self._assess_investment_readiness(client_info, transactions, transfers),
            'risk_profile': self._assess_risk_profile(transactions, transfers)
        }
        
        return patterns
    
    def _get_transactions_period(self, client_code: str, days: int) -> List[Dict]:
        """Получить транзакции за период"""
        query = """
        SELECT t.*, c.name as client_name
        FROM "Transactions" t
        JOIN "Clients" c ON t.client_code = c.client_code
        WHERE t.client_code = %s 
        AND t.date >= CURRENT_DATE - INTERVAL '%s days'
        ORDER BY t.date DESC
        """
        return self.db.execute_query(query, (client_code, days))
    
    def _get_transfers_period(self, client_code: str, days: int) -> List[Dict]:
        """Получить переводы за период"""
        query = """
        SELECT tr.*, c.name as client_name
        FROM "Transfers" tr
        JOIN "Clients" c ON tr.client_code = c.client_code
        WHERE tr.client_code = %s 
        AND tr.date >= CURRENT_DATE - INTERVAL '%s days'
        ORDER BY tr.date DESC
        """
        return self.db.execute_query(query, (client_code, days))
    
    def _detect_spending_patterns(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Детекция паттернов трат"""
        if not transactions:
            return {}
        
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        patterns = {}
        
        # Анализ категорий трат
        category_analysis = df.groupby('category')['amount'].sum().sort_values(ascending=False)
        total_spending = df['amount'].sum()
        
        # Топ категории по сумме
        top_categories = category_analysis.head(5).to_dict()
        patterns['top_categories'] = top_categories
        
        # Доли категорий
        category_shares = {}
        for category, amount in category_analysis.items():
            category_shares[category] = round((amount / total_spending) * 100, 2)
        patterns['category_shares'] = category_shares
        
        # Специфические паттерны
        patterns['high_taxi_spending'] = self._check_high_category_spending(df, ['такси', 'uber', 'yandex'], 20)
        patterns['high_travel_spending'] = self._check_high_category_spending(df, ['путешествия', 'авиабилеты', 'отели'], 15)
        patterns['high_restaurant_spending'] = self._check_high_category_spending(df, ['ресторан', 'кафе', 'еда'], 25)
        patterns['luxury_spending'] = self._check_high_category_spending(df, ['ювелирные', 'парфюмерия', 'премиум'], 10)
        
        return patterns
    
    def _detect_financial_behavior(self, transactions: List[Dict], transfers: List[Dict]) -> Dict[str, Any]:
        """Детекция финансового поведения"""
        behavior = {}
        
        # Анализ транзакций
        if transactions:
            df_trans = pd.DataFrame(transactions)
            df_trans['amount'] = pd.to_numeric(df_trans['amount'])
            
            behavior['avg_transaction_size'] = df_trans['amount'].mean()
            behavior['transaction_frequency'] = len(transactions) / 30  # В месяц
            behavior['large_transactions'] = len(df_trans[df_trans['amount'] > df_trans['amount'].quantile(0.9)])
        
        # Анализ переводов
        if transfers:
            df_transfers = pd.DataFrame(transfers)
            df_transfers['amount'] = pd.to_numeric(df_transfers['amount'])
            
            behavior['avg_transfer_size'] = df_transfers['amount'].mean()
            behavior['transfer_frequency'] = len(transfers) / 30  # В месяц
            
            # Анализ входящих vs исходящих
            if 'direction' in df_transfers.columns:
                incoming = df_transfers[df_transfers['direction'] == 'incoming']
                outgoing = df_transfers[df_transfers['direction'] == 'outgoing']
                
                behavior['incoming_ratio'] = len(incoming) / len(transfers) if transfers else 0
                behavior['outgoing_ratio'] = len(outgoing) / len(transfers) if transfers else 0
        
        return behavior
    
    def _detect_lifestyle_signals(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Детекция сигналов образа жизни"""
        if not transactions:
            return {}
        
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        signals = {}
        
        # Анализ по времени (если есть поле time)
        if 'time' in df.columns:
            df['hour'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce').dt.hour
            night_transactions = df[(df['hour'] >= 22) | (df['hour'] <= 6)]
            signals['night_activity'] = len(night_transactions) > 0
        
        # Анализ по дням недели
        df['weekday'] = df['date'].dt.day_name()
        weekend_transactions = df[df['weekday'].isin(['Saturday', 'Sunday'])]
        signals['weekend_activity'] = len(weekend_transactions) > 0
        
        # Анализ регулярности трат
        monthly_spending = df.groupby(df['date'].dt.to_period('M'))['amount'].sum()
        signals['spending_regularity'] = len(monthly_spending) >= 2
        
        return signals
    
    def _assess_investment_readiness(self, client_info: Dict, transactions: List[Dict], transfers: List[Dict]) -> Dict[str, Any]:
        """Оценка готовности к инвестициям"""
        readiness = {}
        
        # Анализ баланса
        avg_balance = client_info.get('avg_monthly_balance_kzt', 0)
        readiness['has_high_balance'] = avg_balance > 1000000  # 1 млн тенге
        readiness['has_very_high_balance'] = avg_balance > 6000000  # 6 млн тенге
        
        # Анализ свободных денег
        if transactions:
            df_trans = pd.DataFrame(transactions)
            df_trans['amount'] = pd.to_numeric(df_trans['amount'])
            
            # Если есть крупные траты, значит есть свободные деньги
            large_spending = df_trans[df_trans['amount'] > df_trans['amount'].quantile(0.8)]
            readiness['has_disposable_income'] = len(large_spending) > 0
        
        # Анализ сбережений
        if transfers:
            df_transfers = pd.DataFrame(transfers)
            df_transfers['amount'] = pd.to_numeric(df_transfers['amount'])
            
            # Ищем переводы на сбережения
            savings_keywords = ['вклад', 'депозит', 'сбережения', 'savings']
            savings_transfers = df_transfers[
                df_transfers['type'].str.lower().str.contains('|'.join(savings_keywords), na=False)
            ]
            readiness['has_savings_behavior'] = len(savings_transfers) > 0
        
        return readiness
    
    def _assess_risk_profile(self, transactions: List[Dict], transfers: List[Dict]) -> Dict[str, Any]:
        """Оценка профиля риска"""
        risk_profile = {
            'risk_level': 'conservative',  # По умолчанию консервативный
            'indicators': []
        }
        
        # Анализ волатильности трат
        if transactions:
            df_trans = pd.DataFrame(transactions)
            df_trans['amount'] = pd.to_numeric(df_trans['amount'])
            
            # Высокая волатильность = агрессивный профиль
            if df_trans['amount'].std() > df_trans['amount'].mean():
                risk_profile['indicators'].append('high_spending_volatility')
                risk_profile['risk_level'] = 'aggressive'
        
        # Анализ частоты операций
        total_operations = len(transactions) + len(transfers)
        if total_operations > 50:  # Много операций
            risk_profile['indicators'].append('high_activity')
            if risk_profile['risk_level'] == 'conservative':
                risk_profile['risk_level'] = 'moderate'
        
        return risk_profile
    
    def _check_high_category_spending(self, df: pd.DataFrame, keywords: List[str], threshold_percent: float) -> bool:
        """Проверить высокие траты по категории"""
        if df.empty:
            return False
        
        # Ищем транзакции по ключевым словам
        matching_transactions = df[
            df['category'].str.lower().str.contains('|'.join(keywords), na=False)
        ]
        
        if matching_transactions.empty:
            return False
        
        # Проверяем долю от общих трат
        total_spending = df['amount'].sum()
        category_spending = matching_transactions['amount'].sum()
        
        return (category_spending / total_spending) * 100 >= threshold_percent
    
    def generate_client_signals(self, client_code: str, days: int = 90) -> List[Dict[str, Any]]:
        """
        Генерация сигналов для клиента на основе паттернов
        
        Returns:
            Список сигналов с их силой и описанием
        """
        patterns = self.detect_client_patterns(client_code, days)
        signals = []
        
        # Сигналы на основе трат
        spending_patterns = patterns.get('spending_patterns', {})
        
        # Сигнал для карты путешествий
        if (spending_patterns.get('high_taxi_spending', False) or 
            spending_patterns.get('high_travel_spending', False)):
            signals.append({
                'signal': 'travel_card_candidate',
                'strength': 0.8,
                'description': 'Клиент часто тратит на такси и путешествия',
                'category': 'travel'
            })
        
        # Сигнал для премиальной карты
        client_info = patterns.get('client_info', {})
        avg_balance = client_info.get('avg_monthly_balance_kzt', 0)
        if avg_balance > 6000000:  # 6 млн тенге
            signals.append({
                'signal': 'premium_card_candidate',
                'strength': 0.9,
                'description': 'Клиент имеет высокий средний баланс',
                'category': 'premium'
            })
        
        # Сигнал для кредитной карты
        if spending_patterns.get('high_restaurant_spending', False):
            signals.append({
                'signal': 'credit_card_candidate',
                'strength': 0.7,
                'description': 'Клиент часто тратит в ресторанах',
                'category': 'credit'
            })
        
        # Сигнал для валютных операций
        currency_analysis = self._analyze_currency_operations(client_code, days)
        if currency_analysis.get('has_currency_operations', False):
            signals.append({
                'signal': 'currency_exchange_candidate',
                'strength': 0.8,
                'description': 'Клиент часто меняет валюту',
                'category': 'currency'
            })
        
        # Сигнал для депозитов
        investment_readiness = patterns.get('investment_readiness', {})
        if investment_readiness.get('has_high_balance', False):
            signals.append({
                'signal': 'deposit_candidate',
                'strength': 0.8,
                'description': 'Клиент имеет свободные деньги для депозита',
                'category': 'deposit'
            })
        
        return signals
    
    def _analyze_currency_operations(self, client_code: str, days: int) -> Dict[str, Any]:
        """Анализ валютных операций"""
        transfers = self._get_transfers_period(client_code, days)
        
        if not transfers:
            return {'has_currency_operations': False}
        
        df = pd.DataFrame(transfers)
        
        # Ищем валютные операции
        currency_keywords = ['usd', 'eur', 'rub', 'валют', 'currency', 'обмен', 'exchange']
        
        currency_transfers = df[
            df['type'].str.lower().str.contains('|'.join(currency_keywords), na=False) |
            df['description'].str.lower().str.contains('|'.join(currency_keywords), na=False)
        ]
        
        return {
            'has_currency_operations': len(currency_transfers) > 0,
            'frequency': len(currency_transfers) / days * 30  # Операций в месяц
        }
