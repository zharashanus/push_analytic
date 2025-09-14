"""
Скрипт для инициализации базы данных аналитики
Подключение к удаленной базе данных Neon
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from src.config import db_config


def create_tables():
    """Создание таблиц в существующей базе данных"""
    
    try:
        # Подключаемся к Neon DB
        conn = psycopg2.connect(db_config.get_connection_string())
        cursor = conn.cursor()
        
        # Создаем таблицы
        create_tables_sql(cursor)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Таблицы созданы успешно в Neon DB")
        
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")


def create_tables_sql(cursor):
    """SQL для создания таблиц"""
    
    # Таблица клиентов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Clients" (
            id SERIAL PRIMARY KEY,
            client_code VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            status VARCHAR(100) NOT NULL,
            age INTEGER,
            city VARCHAR(100),
            avg_monthly_balance_KZT DECIMAL(15,2) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Таблица транзакций
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Transactions" (
            id SERIAL PRIMARY KEY,
            client_code VARCHAR(50) NOT NULL,
            date DATE NOT NULL,
            category VARCHAR(255) NOT NULL,
            amount DECIMAL(15,2) NOT NULL,
            currency VARCHAR(10) DEFAULT 'KZT',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_code) REFERENCES "Clients"(client_code)
        )
    """)
    
    # Таблица переводов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Transfers" (
            id SERIAL PRIMARY KEY,
            client_code VARCHAR(50) NOT NULL,
            date DATE NOT NULL,
            type VARCHAR(100) NOT NULL,
            direction VARCHAR(10) NOT NULL CHECK (direction IN ('in', 'out')),
            amount DECIMAL(15,2) NOT NULL,
            currency VARCHAR(10) DEFAULT 'KZT',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_code) REFERENCES "Clients"(client_code)
        )
    """)
    
    # Таблица выгод от продуктов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "ProductBenefits" (
            id SERIAL PRIMARY KEY,
            client_code VARCHAR(50) NOT NULL,
            product VARCHAR(255) NOT NULL,
            expected_benefit DECIMAL(15,2) NOT NULL,
            score DECIMAL(3,2) NOT NULL,
            reasons TEXT[],
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_code) REFERENCES "Clients"(client_code)
        )
    """)
    
    # Создаем индексы для производительности
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_client_code ON \"Transactions\"(client_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_date ON \"Transactions\"(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_category ON \"Transactions\"(category)")
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transfers_client_code ON \"Transfers\"(client_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transfers_date ON \"Transfers\"(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transfers_type ON \"Transfers\"(type)")
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_benefits_client_code ON \"ProductBenefits\"(client_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_benefits_product ON \"ProductBenefits\"(product)")


def insert_sample_data():
    """Вставка тестовых данных"""
    
    try:
        conn = psycopg2.connect(db_config.get_connection_string())
        cursor = conn.cursor()
        
        # Проверяем, есть ли уже данные
        cursor.execute("SELECT COUNT(*) FROM \"Clients\"")
        if cursor.fetchone()[0] > 0:
            print("Тестовые данные уже существуют")
            return
        
        # Вставляем тестового клиента
        cursor.execute("""
            INSERT INTO "Clients" (client_code, name, status, age, city, avg_monthly_balance_KZT)
            VALUES ('12345', 'Рамазан', 'Зарплатный клиент', 30, 'Алматы', 240000)
        """)
        
        # Вставляем тестовые транзакции
        cursor.execute("""
            INSERT INTO "Transactions" (client_code, date, category, amount, currency)
            VALUES 
                ('12345', '2025-08-10', 'Такси', 27400, 'KZT'),
                ('12345', '2025-08-12', 'Продукты питания', 44000, 'KZT'),
                ('12345', '2025-08-15', 'Отели', 150000, 'KZT'),
                ('12345', '2025-08-20', 'Путешествия', 80000, 'KZT')
        """)
        
        # Вставляем тестовые переводы
        cursor.execute("""
            INSERT INTO "Transfers" (client_code, date, type, direction, amount, currency)
            VALUES 
                ('12345', '2025-08-01', 'salary_in', 'in', 320000, 'KZT'),
                ('12345', '2025-08-05', 'p2p_out', 'out', 50000, 'KZT'),
                ('12345', '2025-08-10', 'atm_withdrawal', 'out', 20000, 'KZT')
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Тестовые данные добавлены успешно")
        
    except Exception as e:
        print(f"Ошибка при добавлении тестовых данных: {e}")


def test_connection():
    """Тест подключения к базе данных"""
    
    try:
        conn = psycopg2.connect(db_config.get_connection_string())
        cursor = conn.cursor()
        
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"Подключение к базе данных успешно: {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return False


if __name__ == "__main__":
    print("Инициализация базы данных push_analytic...")
    print(f"Подключение к: {db_config.host}")
    
    if test_connection():
        create_tables()
        insert_sample_data()
        print("Готово!")
    else:
        print("Не удалось подключиться к базе данных")
