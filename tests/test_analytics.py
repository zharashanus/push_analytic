"""
Тесты для слоя аналитики
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Добавляем путь к src для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from analytics.transaction_analyzer import TransactionAnalyzer
from analytics.transfer_analyzer import TransferAnalyzer
from analytics.pattern_detector import PatternDetector


class TestTransactionAnalyzer(unittest.TestCase):
    """Тесты для анализатора транзакций"""
    
    def setUp(self):
        """Настройка тестов"""
        self.mock_db = Mock()
        self.analyzer = TransactionAnalyzer(self.mock_db)
    
    def test_empty_analysis(self):
        """Тест пустого анализа"""
        self.mock_db.execute_query.return_value = []
        
        result = self.analyzer.analyze_client_transactions('TEST001', 90)
        
        self.assertEqual(result['total_transactions'], 0)
        self.assertEqual(result['total_amount'], 0)
        self.assertEqual(result['client_code'], 'TEST001')
    
    def test_categories_analysis(self):
        """Тест анализа категорий"""
        # Мокаем данные транзакций
        mock_transactions = [
            {'category': 'такси', 'amount': 1000, 'date': '2024-01-01'},
            {'category': 'такси', 'amount': 1500, 'date': '2024-01-02'},
            {'category': 'ресторан', 'amount': 2000, 'date': '2024-01-03'},
            {'category': 'продукты', 'amount': 500, 'date': '2024-01-04'}
        ]
        
        self.mock_db.execute_query.return_value = mock_transactions
        
        result = self.analyzer.analyze_client_transactions('TEST001', 90)
        
        # Проверяем анализ категорий
        categories = result['categories_analysis']
        self.assertIn('такси', categories['top_by_count'])
        self.assertEqual(categories['top_by_count']['такси'], 2)
        
        # Проверяем доли категорий
        self.assertIn('такси', categories['category_shares'])
        self.assertIn('ресторан', categories['category_shares'])


class TestTransferAnalyzer(unittest.TestCase):
    """Тесты для анализатора переводов"""
    
    def setUp(self):
        """Настройка тестов"""
        self.mock_db = Mock()
        self.analyzer = TransferAnalyzer(self.mock_db)
    
    def test_empty_analysis(self):
        """Тест пустого анализа"""
        self.mock_db.execute_query.return_value = []
        
        result = self.analyzer.analyze_client_transfers('TEST001', 90)
        
        self.assertEqual(result['total_transfers'], 0)
        self.assertEqual(result['total_amount'], 0)
        self.assertFalse(result['salary_analysis']['has_salary'])
    
    def test_salary_analysis(self):
        """Тест анализа зарплат"""
        mock_transfers = [
            {'type': 'зарплата', 'amount': 500000, 'date': '2024-01-01', 'description': 'Зарплата за январь'},
            {'type': 'перевод', 'amount': 10000, 'date': '2024-01-02', 'description': 'Перевод другу'}
        ]
        
        self.mock_db.execute_query.return_value = mock_transfers
        
        result = self.analyzer.analyze_client_transfers('TEST001', 90)
        
        # Проверяем анализ зарплат
        salary_analysis = result['salary_analysis']
        self.assertTrue(salary_analysis['has_salary'])
        self.assertEqual(salary_analysis['total_amount'], 500000)
        self.assertEqual(salary_analysis['transaction_count'], 1)


class TestPatternDetector(unittest.TestCase):
    """Тесты для детектора паттернов"""
    
    def setUp(self):
        """Настройка тестов"""
        self.mock_db = Mock()
        self.detector = PatternDetector(self.mock_db)
    
    def test_empty_patterns(self):
        """Тест пустых паттернов"""
        self.mock_db.get_client_by_code.return_value = None
        
        result = self.detector.detect_client_patterns('TEST001', 90)
        
        self.assertEqual(result, {})
    
    def test_client_signals(self):
        """Тест генерации сигналов"""
        # Мокаем данные клиента
        mock_client = {
            'client_code': 'TEST001',
            'name': 'Test Client',
            'avg_monthly_balance_kzt': 7000000  # 7 млн тенге
        }
        
        self.mock_db.get_client_by_code.return_value = mock_client
        self.mock_db.execute_query.return_value = []
        
        signals = self.detector.generate_client_signals('TEST001', 90)
        
        # Проверяем, что есть сигнал для премиальной карты
        premium_signals = [s for s in signals if s['signal'] == 'premium_card_candidate']
        self.assertTrue(len(premium_signals) > 0)
        self.assertEqual(premium_signals[0]['strength'], 0.9)


if __name__ == '__main__':
    unittest.main()
