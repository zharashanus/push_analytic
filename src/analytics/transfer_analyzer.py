"""
Анализатор переводов клиента
"""

from datetime import datetime, timedelta
from collections import Counter
from typing import Dict, List, Any, Optional
import pandas as pd


class TransferAnalyzer:
    """Анализатор переводов для выявления паттернов движения денег"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def analyze_client_transfers(self, client_code: str, days: int = 90) -> Dict[str, Any]:
        """
        Полный анализ переводов клиента
        
        Args:
            client_code: Код клиента
            days: Период анализа в днях (по умолчанию 90)
        
        Returns:
            Словарь с результатами анализа
        """
        # Получаем переводы за период
        transfers = self._get_transfers_period(client_code, days)
        
        if not transfers:
            return self._empty_analysis()
        
        # Конвертируем в DataFrame для удобства анализа
        df = pd.DataFrame(transfers)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        analysis = {
            'client_code': client_code,
            'period_days': days,
            'total_transfers': len(transfers),
            'total_amount': df['amount'].sum(),
            'avg_transfer': df['amount'].mean(),
            'salary_analysis': self._analyze_salary_transfers(df),
            'deposit_analysis': self._analyze_deposits(df),
            'credit_analysis': self._analyze_credits(df),
            'withdrawal_analysis': self._analyze_withdrawals(df),
            'transfer_patterns': self._detect_transfer_patterns(df)
        }
        
        return analysis
    
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
    
    def _analyze_salary_transfers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализ зарплатных переводов и стипендий"""
        if df.empty:
            return {}
        
        # Ключевые слова для зарплат и стипендий
        salary_keywords = ['зарплата', 'salary', 'стипендия', 'scholarship', 'пенсия', 'pension']
        
        # Ищем переводы по ключевым словам
        salary_transfers = df[
            df['type'].str.lower().str.contains('|'.join(salary_keywords), na=False) |
            df['description'].str.lower().str.contains('|'.join(salary_keywords), na=False)
        ]
        
        if salary_transfers.empty:
            return {'has_salary': False}
        
        # Группируем по месяцам для выявления регулярности
        monthly_salary = salary_transfers.groupby(
            salary_transfers['date'].dt.to_period('M')
        )['amount'].sum()
        
        return {
            'has_salary': True,
            'total_amount': salary_transfers['amount'].sum(),
            'transaction_count': len(salary_transfers),
            'avg_monthly': monthly_salary.mean(),
            'monthly_data': monthly_salary.to_dict(),
            'is_regular': len(monthly_salary) >= 2,
            'last_salary_date': salary_transfers['date'].max().strftime('%Y-%m-%d')
        }
    
    def _analyze_deposits(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализ вкладов и депозитов"""
        if df.empty:
            return {}
        
        # Ключевые слова для вкладов
        deposit_keywords = ['вклад', 'депозит', 'deposit', 'сбережения', 'savings']
        
        # Ищем переводы по ключевым словам
        deposit_transfers = df[
            df['type'].str.lower().str.contains('|'.join(deposit_keywords), na=False) |
            df['description'].str.lower().str.contains('|'.join(deposit_keywords), na=False)
        ]
        
        if deposit_transfers.empty:
            return {'has_deposits': False}
        
        return {
            'has_deposits': True,
            'total_amount': deposit_transfers['amount'].sum(),
            'transaction_count': len(deposit_transfers),
            'avg_amount': deposit_transfers['amount'].mean(),
            'max_amount': deposit_transfers['amount'].max(),
            'last_deposit_date': deposit_transfers['date'].max().strftime('%Y-%m-%d')
        }
    
    def _analyze_credits(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализ кредитов и займов"""
        if df.empty:
            return {}
        
        # Ключевые слова для кредитов
        credit_keywords = ['кредит', 'займ', 'credit', 'loan', 'рассрочка', 'installment']
        
        # Ищем переводы по ключевым словам
        credit_transfers = df[
            df['type'].str.lower().str.contains('|'.join(credit_keywords), na=False) |
            df['description'].str.lower().str.contains('|'.join(credit_keywords), na=False)
        ]
        
        if credit_transfers.empty:
            return {'has_credits': False}
        
        return {
            'has_credits': True,
            'total_amount': credit_transfers['amount'].sum(),
            'transaction_count': len(credit_transfers),
            'avg_amount': credit_transfers['amount'].mean(),
            'max_amount': credit_transfers['amount'].max(),
            'last_credit_date': credit_transfers['date'].max().strftime('%Y-%m-%d')
        }
    
    def _analyze_withdrawals(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализ снятий наличных"""
        if df.empty:
            return {}
        
        # Ключевые слова для снятий
        withdrawal_keywords = ['снятие', 'наличные', 'withdrawal', 'cash', 'банкомат', 'atm']
        
        # Ищем переводы по ключевым словам
        withdrawal_transfers = df[
            df['type'].str.lower().str.contains('|'.join(withdrawal_keywords), na=False) |
            df['description'].str.lower().str.contains('|'.join(withdrawal_keywords), na=False)
        ]
        
        if withdrawal_transfers.empty:
            return {'has_withdrawals': False}
        
        # Анализ частоты снятий
        monthly_withdrawals = withdrawal_transfers.groupby(
            withdrawal_transfers['date'].dt.to_period('M')
        )['amount'].sum()
        
        return {
            'has_withdrawals': True,
            'total_amount': withdrawal_transfers['amount'].sum(),
            'transaction_count': len(withdrawal_transfers),
            'avg_amount': withdrawal_transfers['amount'].mean(),
            'avg_monthly': monthly_withdrawals.mean(),
            'monthly_data': monthly_withdrawals.to_dict(),
            'is_frequent': len(monthly_withdrawals) >= 2
        }
    
    def _detect_transfer_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Выявление паттернов переводов"""
        if df.empty:
            return {}
        
        patterns = {}
        
        # Анализ по типам переводов
        type_counts = df['type'].value_counts().to_dict()
        patterns['transfer_types'] = type_counts
        
        # Анализ по дням недели
        df['weekday'] = df['date'].dt.day_name()
        weekday_transfers = df.groupby('weekday')['amount'].sum().to_dict()
        patterns['weekday_pattern'] = weekday_transfers
        
        # Анализ крупных переводов
        large_transfers = df[df['amount'] > df['amount'].quantile(0.9)]
        patterns['large_transfers'] = {
            'count': len(large_transfers),
            'total_amount': large_transfers['amount'].sum(),
            'avg_amount': large_transfers['amount'].mean()
        }
        
        # Анализ входящих vs исходящих переводов
        if 'direction' in df.columns:
            incoming = df[df['direction'] == 'incoming']
            outgoing = df[df['direction'] == 'outgoing']
            
            patterns['transfer_direction'] = {
                'incoming': {
                    'count': len(incoming),
                    'total_amount': incoming['amount'].sum()
                },
                'outgoing': {
                    'count': len(outgoing),
                    'total_amount': outgoing['amount'].sum()
                }
            }
        
        return patterns
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Пустой анализ для клиентов без переводов"""
        return {
            'client_code': '',
            'period_days': 0,
            'total_transfers': 0,
            'total_amount': 0,
            'avg_transfer': 0,
            'salary_analysis': {'has_salary': False},
            'deposit_analysis': {'has_deposits': False},
            'credit_analysis': {'has_credits': False},
            'withdrawal_analysis': {'has_withdrawals': False},
            'transfer_patterns': {}
        }
    
    def get_currency_analysis(self, client_code: str, days: int = 90) -> Dict[str, Any]:
        """Анализ валютных операций клиента"""
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
        
        if currency_transfers.empty:
            return {'has_currency_operations': False}
        
        return {
            'has_currency_operations': True,
            'total_amount': currency_transfers['amount'].sum(),
            'transaction_count': len(currency_transfers),
            'avg_amount': currency_transfers['amount'].mean(),
            'frequency': len(currency_transfers) / days * 30  # Операций в месяц
        }
