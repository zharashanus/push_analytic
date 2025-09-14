"""
Конфигурация базы данных для аналитики
Подключение к удаленной базе данных Neon
"""

import os
from typing import Optional


class DatabaseConfig:
    """Конфигурация подключения к удаленной базе данных Neon"""
    
    def __init__(self):
        # Используем переменные окружения для Neon DB
        self.host = os.getenv('PGHOST', 'ep-little-tree-agjwpa12-pooler.c-2.eu-central-1.aws.neon.tech')
        self.port = int(os.getenv('PGPORT', '5432'))
        self.database = os.getenv('PGDATABASE', 'neondb')
        self.user = os.getenv('PGUSER', 'neondb_owner')
        self.password = os.getenv('PGPASSWORD', 'npg_PJH1k4RZXAux')
        self.sslmode = os.getenv('PGSSLMODE', 'require')
        self.channel_binding = os.getenv('PGCHANNELBINDING', 'require')
        
        # Получаем полную строку подключения если есть
        self.database_url = os.getenv('DATABASE_URL')
    
    def get_connection_string(self) -> str:
        """Получить строку подключения к базе данных"""
        if self.database_url:
            return self.database_url
        
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?sslmode={self.sslmode}&channel_binding={self.channel_binding}"
    
    def get_connection_params(self) -> dict:
        """Получить параметры подключения"""
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'password': self.password,
            'sslmode': self.sslmode,
            'channel_binding': self.channel_binding
        }


# Глобальный экземпляр конфигурации
db_config = DatabaseConfig()
