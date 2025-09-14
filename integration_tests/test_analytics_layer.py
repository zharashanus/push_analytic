"""
Тест слоя аналитики
"""

import sys
import os
import unittest
from datetime import datetime

# Добавляем путь к src для импорта модулей
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from database import db_manager
from analytics.transaction_analyzer import TransactionAnalyzer
from analytics.transfer_analyzer import TransferAnalyzer
from analytics.pattern_detector import PatternDetector


class TestAnalyticsLayer(unittest.TestCase):
    """Тесты слоя аналитики"""
    
    def setUp(self):
        """Настройка тестов"""
        self.transaction_analyzer = TransactionAnalyzer(db_manager)
        self.transfer_analyzer = TransferAnalyzer(db_manager)
        self.pattern_detector = PatternDetector(db_manager)
        
        # Получаем реального клиента для тестирования
        clients = db_manager.get_clients(limit=1)
        if clients:
            self.test_client_code = clients[0]['client_code']
        else:
            self.test_client_code = None
    
    def test_transaction_analyzer(self):
        """Тест анализатора транзакций"""
        print("🔍 Тестирование анализатора транзакций...")
        
        if not self.test_client_code:
            self.skipTest("Нет клиентов для тестирования")
        
        # Тест анализа транзакций
        analysis = self.transaction_analyzer.analyze_client_transactions(
            self.test_client_code, 90
        )
        
        self.assertIsNotNone(analysis, "Анализ транзакций не выполнен")
        self.assertIn('client_code', analysis, "Отсутствует код клиента в анализе")
        self.assertIn('total_transactions', analysis, "Отсутствует количество транзакций")
        self.assertIn('total_amount', analysis, "Отсутствует общая сумма")
        
        print(f"   ✅ Анализ транзакций для клиента {self.test_client_code}")
        print(f"   📊 Транзакций: {analysis['total_transactions']}")
        print(f"   💰 Сумма: {analysis['total_amount']:,.0f} ₸")
        
        # Тест получения информации о балансе
        balance_info = self.transaction_analyzer.get_client_balance_info(self.test_client_code)
        self.assertIsNotNone(balance_info, "Информация о балансе не получена")
        print(f"   💳 Средний баланс: {balance_info.get('avg_monthly_balance', 0):,.0f} ₸")
    
    def test_transfer_analyzer(self):
        """Тест анализатора переводов"""
        print("💸 Тестирование анализатора переводов...")
        
        if not self.test_client_code:
            self.skipTest("Нет клиентов для тестирования")
        
        # Тест анализа переводов
        analysis = self.transfer_analyzer.analyze_client_transfers(
            self.test_client_code, 90
        )
        
        self.assertIsNotNone(analysis, "Анализ переводов не выполнен")
        self.assertIn('client_code', analysis, "Отсутствует код клиента в анализе")
        self.assertIn('total_transfers', analysis, "Отсутствует количество переводов")
        self.assertIn('total_amount', analysis, "Отсутствует общая сумма")
        
        print(f"   ✅ Анализ переводов для клиента {self.test_client_code}")
        print(f"   📊 Переводов: {analysis['total_transfers']}")
        print(f"   💰 Сумма: {analysis['total_amount']:,.0f} ₸")
        
        # Тест анализа валютных операций
        currency_analysis = self.transfer_analyzer.get_currency_analysis(
            self.test_client_code, 90
        )
        self.assertIsNotNone(currency_analysis, "Анализ валютных операций не выполнен")
        print(f"   🌍 Валютные операции: {'Да' if currency_analysis.get('has_currency_operations') else 'Нет'}")
    
    def test_pattern_detector(self):
        """Тест детектора паттернов"""
        print("🎯 Тестирование детектора паттернов...")
        
        if not self.test_client_code:
            self.skipTest("Нет клиентов для тестирования")
        
        # Тест детекции паттернов
        patterns = self.pattern_detector.detect_client_patterns(
            self.test_client_code, 90
        )
        
        self.assertIsNotNone(patterns, "Детекция паттернов не выполнена")
        self.assertIn('client_code', patterns, "Отсутствует код клиента в паттернах")
        self.assertIn('client_info', patterns, "Отсутствует информация о клиенте")
        
        print(f"   ✅ Паттерны для клиента {self.test_client_code}")
        
        # Тест генерации сигналов
        signals = self.pattern_detector.generate_client_signals(
            self.test_client_code, 90
        )
        
        self.assertIsNotNone(signals, "Генерация сигналов не выполнена")
        self.assertIsInstance(signals, list, "Сигналы должны быть списком")
        
        print(f"   🚦 Найдено сигналов: {len(signals)}")
        for signal in signals:
            print(f"      • {signal['description']} (сила: {signal['strength']})")
    
    def test_analytics_integration(self):
        """Интеграционный тест всей аналитики"""
        print("🔄 Интеграционный тест аналитики...")
        
        if not self.test_client_code:
            self.skipTest("Нет клиентов для тестирования")
        
        # Полный цикл анализа
        print(f"   📋 Анализ клиента: {self.test_client_code}")
        
        # 1. Анализ транзакций
        transaction_analysis = self.transaction_analyzer.analyze_client_transactions(
            self.test_client_code, 90
        )
        
        # 2. Анализ переводов
        transfer_analysis = self.transfer_analyzer.analyze_client_transfers(
            self.test_client_code, 90
        )
        
        # 3. Детекция паттернов
        patterns = self.pattern_detector.detect_client_patterns(
            self.test_client_code, 90
        )
        
        # 4. Генерация сигналов
        signals = self.pattern_detector.generate_client_signals(
            self.test_client_code, 90
        )
        
        # Проверяем, что все компоненты работают
        self.assertIsNotNone(transaction_analysis)
        self.assertIsNotNone(transfer_analysis)
        self.assertIsNotNone(patterns)
        self.assertIsNotNone(signals)
        
        print("   ✅ Полный цикл анализа выполнен успешно")
        
        # Выводим сводку
        print(f"   📊 Результаты анализа:")
        print(f"      • Транзакций: {transaction_analysis['total_transactions']}")
        print(f"      • Переводов: {transfer_analysis['total_transfers']}")
        print(f"      • Сигналов: {len(signals)}")
        
        if patterns.get('client_info'):
            balance = patterns['client_info'].get('avg_monthly_balance_kzt', 0)
            print(f"      • Средний баланс: {balance:,.0f} ₸")


if __name__ == '__main__':
    print("🚀 Запуск тестов слоя аналитики...")
    unittest.main(verbosity=2)
