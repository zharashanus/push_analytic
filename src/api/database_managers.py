"""
Менеджеры базы данных для API
"""

from typing import Dict, List, Any
import psycopg2
from ..config.database import db_config


class MockDatabaseManager:
    """Мок-менеджер базы данных для тестирования"""
    
    def __init__(self, client_info: Dict, transactions: List[Dict], transfers: List[Dict]):
        self.client_info = client_info
        self.transactions = transactions
        self.transfers = transfers
    
    def get_client_by_code(self, client_code: str) -> Dict:
        """Получить данные клиента"""
        if str(self.client_info['client_code']) == str(client_code):
            return self.client_info
        return {}
    
    def execute_query(self, query: str, params: tuple) -> List[Dict]:
        """Выполнить SQL запрос"""
        if 'Transactions' in query:
            return self.transactions
        elif 'Transfers' in query:
            return self.transfers
        return []


class RealDatabaseManager:
    """Реальный менеджер базы данных для работы с Neon DB"""
    
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Подключение к базе данных"""
        try:
            self.connection = psycopg2.connect(
                host=db_config.host,
                port=db_config.port,
                database=db_config.database,
                user=db_config.user,
                password=db_config.password,
                sslmode=db_config.sslmode
            )
            print("✅ Подключение к базе данных установлено")
        except Exception as e:
            print(f"❌ Ошибка подключения к БД: {e}")
            self.connection = None
    
    def get_client_by_code(self, client_code: str) -> Dict:
        """Получить данные клиента из БД"""
        if not self.connection:
            return {}
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT client_code, name, status, avg_monthly_balance_KZT, city, age
                    FROM "Clients" 
                    WHERE client_code = %s
                """, (client_code,))
                
                result = cursor.fetchone()
                if result:
                    return {
                        'client_code': result[0],
                        'name': result[1],
                        'status': result[2],
                        'avg_monthly_balance_KZT': float(result[3]) if result[3] else 0,
                        'city': result[4] or 'Алматы',
                        'age': result[5] or 30
                    }
                return {}
        except Exception as e:
            print(f"Ошибка получения клиента: {e}")
            return {}
    
    def execute_query(self, query: str, params: tuple) -> List[Dict]:
        """Выполнить SQL запрос"""
        if not self.connection:
            return []
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                
                # Получаем названия колонок
                columns = [desc[0] for desc in cursor.description]
                
                # Преобразуем результаты в список словарей
                results = []
                for row in cursor.fetchall():
                    row_dict = {}
                    for i, value in enumerate(row):
                        row_dict[columns[i]] = value
                    results.append(row_dict)
                
                return results
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return []
    
    def get_random_client_code(self) -> str:
        """Получить случайный код клиента из БД"""
        if not self.connection:
            print("❌ Нет подключения к БД")
            return None
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT client_code 
                    FROM "Clients" 
                    ORDER BY RANDOM() 
                    LIMIT 1
                """)
                
                result = cursor.fetchone()
                if result and result[0]:
                    client_code = str(result[0])
                    print(f"✅ Найден случайный клиент: {client_code}")
                    return client_code
                else:
                    print("❌ Клиенты не найдены в БД")
                    return None
        except Exception as e:
            print(f"❌ Ошибка получения случайного клиента: {e}")
            return None
    
    def close(self):
        """Закрыть соединение с БД"""
        if self.connection:
            self.connection.close()
