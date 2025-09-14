"""
Тест подключения к базе данных
"""

import sys
import os
import unittest
from datetime import datetime

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import db_manager


class TestDatabaseConnection(unittest.TestCase):
    """Тесты подключения к базе данных"""
    
    def test_database_connection(self):
        """Тест подключения к БД"""
        print("🔌 Тестирование подключения к базе данных...")
        
        # Проверяем подключение
        conn = db_manager.get_connection()
        self.assertIsNotNone(conn, "Не удалось подключиться к базе данных")
        
        # Проверяем, что подключение активно
        self.assertFalse(conn.closed, "Подключение к БД закрыто")
        
        print("✅ Подключение к базе данных успешно")
    
    def test_database_tables_exist(self):
        """Тест существования основных таблиц"""
        print("📋 Проверка существования таблиц...")
        
        # Список обязательных таблиц
        required_tables = ['Clients', 'Transactions', 'Transfers', 'products']
        
        for table in required_tables:
            query = f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            )
            """
            result = db_manager.execute_query(query, (table,))
            self.assertTrue(result[0]['exists'], f"Таблица {table} не существует")
            print(f"   ✅ Таблица {table} существует")
    
    def test_database_data_access(self):
        """Тест доступа к данным"""
        print("📊 Тестирование доступа к данным...")
        
        # Тест получения клиентов
        clients = db_manager.get_clients(limit=5)
        self.assertIsNotNone(clients, "Не удалось получить список клиентов")
        print(f"   ✅ Получено {len(clients)} клиентов")
        
        # Тест получения транзакций
        transactions = db_manager.get_transactions(limit=5)
        self.assertIsNotNone(transactions, "Не удалось получить список транзакций")
        print(f"   ✅ Получено {len(transactions)} транзакций")
        
        # Тест получения переводов
        transfers = db_manager.get_transfers(limit=5)
        self.assertIsNotNone(transfers, "Не удалось получить список переводов")
        print(f"   ✅ Получено {len(transfers)} переводов")
        
        # Тест получения продуктов
        products = db_manager.get_products()
        self.assertIsNotNone(products, "Не удалось получить список продуктов")
        print(f"   ✅ Получено {len(products)} продуктов")
    
    def test_analytics_queries(self):
        """Тест аналитических запросов"""
        print("📈 Тестирование аналитических запросов...")
        
        # Тест аналитической сводки
        analytics = db_manager.get_analytics_summary()
        self.assertIsNotNone(analytics, "Не удалось получить аналитическую сводку")
        
        # Проверяем наличие основных метрик
        expected_metrics = ['total_clients', 'total_transactions', 'total_transfers']
        for metric in expected_metrics:
            self.assertIn(metric, analytics, f"Метрика {metric} отсутствует в аналитике")
            print(f"   ✅ Метрика {metric}: {analytics[metric]}")


if __name__ == '__main__':
    print("🚀 Запуск тестов подключения к базе данных...")
    unittest.main(verbosity=2)
