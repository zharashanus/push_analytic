"""
Анализатор транзакций клиента
"""

from datetime import datetime, timedelta
from collections import Counter
from typing import Dict, List, Any, Optional
import pandas as pd


class TransactionAnalyzer:
    """Анализатор транзакций для выявления паттернов трат клиента"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def analyze_client_transactions(self, client_code: str, days: int = 90) -> Dict[str, Any]:
        """
        Полный анализ транзакций клиента
        
        Args:
            client_code: Код клиента
            days: Период анализа в днях (по умолчанию 90)
        
        Returns:
            Словарь с результатами анализа
        """
        # Получаем транзакции за период
        transactions = self._get_transactions_period(client_code, days)
        
        if not transactions:
            return self._empty_analysis()
        
        # Конвертируем в DataFrame для удобства анализа
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        analysis = {
            'client_code': client_code,
            'period_days': days,
            'total_transactions': len(transactions),
            'total_amount': df['amount'].sum(),
            'avg_transaction': df['amount'].mean(),
            'categories_analysis': self._analyze_categories(df),
            'regular_spending': self._find_regular_spending(df),
            'balance_analysis': self._analyze_balance_patterns(df),
            'spending_patterns': self._detect_spending_patterns(df)
        }
        
        return analysis
    
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
    
    def _analyze_categories(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализ категорий трат"""
        if df.empty:
            return {}
        
        # Топ-3 категории по количеству транзакций
        category_counts = df['category'].value_counts()
        top_categories_count = category_counts.head(3).to_dict()
        
        # Топ-3 категории по сумме трат
        category_amounts = df.groupby('category')['amount'].sum().sort_values(ascending=False)
        top_categories_amount = category_amounts.head(3).to_dict()
        
        # Доли категорий
        total_amount = df['amount'].sum()
        category_shares = {}
        for category, amount in category_amounts.items():
            category_shares[category] = round((amount / total_amount) * 100, 2)
        
        return {
            'top_by_count': top_categories_count,
            'top_by_amount': top_categories_amount,
            'category_shares': category_shares,
            'total_categories': len(category_counts)
        }
    
    def _find_regular_spending(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Поиск регулярных трат (подписки, транспорт, рестораны)"""
        if df.empty:
            return {}
        
        # Категории для регулярных трат
        regular_categories = {
            'subscriptions': ['подписка', 'subscription', 'netflix', 'spotify', 'youtube'],
            'transport': ['такси', 'транспорт', 'uber', 'yandex', 'автобус', 'метро'],
            'restaurants': ['ресторан', 'кафе', 'еда', 'доставка', 'food', 'restaurant']
        }
        
        regular_spending = {}
        
        for category_type, keywords in regular_categories.items():
            # Ищем транзакции по ключевым словам в категории
            matching_transactions = df[
                df['category'].str.lower().str.contains('|'.join(keywords), na=False)
            ]
            
            if not matching_transactions.empty:
                # Группируем по месяцам для выявления регулярности
                monthly_spending = matching_transactions.groupby(
                    matching_transactions['date'].dt.to_period('M')
                )['amount'].sum()
                
                regular_spending[category_type] = {
                    'total_amount': matching_transactions['amount'].sum(),
                    'transaction_count': len(matching_transactions),
                    'avg_monthly': monthly_spending.mean(),
                    'monthly_data': monthly_spending.to_dict(),
                    'is_regular': len(monthly_spending) >= 2  # Регулярно если есть траты в 2+ месяцах
                }
        
        return regular_spending
    
    def _analyze_balance_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализ паттернов баланса"""
        if df.empty:
            return {}
        
        # Анализируем остатки (если есть поле balance)
        balance_analysis = {}
        
        if 'balance' in df.columns:
            balances = df['balance'].dropna()
            if not balances.empty:
                balance_analysis = {
                    'avg_balance': balances.mean(),
                    'min_balance': balances.min(),
                    'max_balance': balances.max(),
                    'balance_volatility': balances.std(),
                    'balance_trend': self._calculate_trend(balances)
                }
        
        return balance_analysis
    
    def _detect_spending_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Выявление паттернов трат"""
        if df.empty:
            return {}
        
        patterns = {}
        
        # Анализ по дням недели
        df['weekday'] = df['date'].dt.day_name()
        weekday_spending = df.groupby('weekday')['amount'].sum().to_dict()
        
        # Анализ по времени суток (если есть поле time)
        if 'time' in df.columns:
            df['hour'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.hour
            hourly_spending = df.groupby('hour')['amount'].sum().to_dict()
            patterns['hourly_pattern'] = hourly_spending
        
        # Анализ крупных трат
        large_transactions = df[df['amount'] > df['amount'].quantile(0.9)]
        patterns['large_transactions'] = {
            'count': len(large_transactions),
            'total_amount': large_transactions['amount'].sum(),
            'avg_amount': large_transactions['amount'].mean()
        }
        
        patterns['weekday_pattern'] = weekday_spending
        
        return patterns
    
    def _calculate_trend(self, series: pd.Series) -> str:
        """Рассчитать тренд данных"""
        if len(series) < 2:
            return 'insufficient_data'
        
        # Простой линейный тренд
        x = range(len(series))
        y = series.values
        
        # Коэффициент наклона
        n = len(x)
        slope = (n * sum(x[i] * y[i] for i in range(n)) - sum(x) * sum(y)) / (n * sum(xi**2 for xi in x) - sum(x)**2)
        
        if slope > 0.1:
            return 'increasing'
        elif slope < -0.1:
            return 'decreasing'
        else:
            return 'stable'
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Пустой анализ для клиентов без транзакций"""
        return {
            'client_code': '',
            'period_days': 0,
            'total_transactions': 0,
            'total_amount': 0,
            'avg_transaction': 0,
            'categories_analysis': {},
            'regular_spending': {},
            'balance_analysis': {},
            'spending_patterns': {}
        }
    
    def get_client_balance_info(self, client_code: str) -> Dict[str, Any]:
        """Получить информацию о балансе клиента"""
        client = self.db.get_client_by_code(client_code)
        if not client:
            return {}
        
        return {
            'avg_monthly_balance': client.get('avg_monthly_balance_kzt', 0),
            'client_name': client.get('name', ''),
            'status': client.get('status', ''),
            'city': client.get('city', '')
        }
