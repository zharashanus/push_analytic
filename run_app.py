"""
Скрипт для запуска Flask приложения
"""

import os
import sys
from flask import Flask
from flask_cors import CORS

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.api.notification_api import app

# Настраиваем CORS для фронтенда на порту 5555
CORS(app, origins=["http://188.244.115.175:5555", "http://localhost:5555"])

if __name__ == "__main__":
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    
    print(f"Запуск push_analytic на порту {port}")
    print(f"Режим отладки: {debug}")
    print(f"База данных: {os.getenv('PGHOST', 'localhost')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
