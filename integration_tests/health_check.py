"""
Проверка здоровья системы
Быстрая проверка основных компонентов перед запуском сервера
"""

import sys
import os
import time
from datetime import datetime

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def health_check():
    """Быстрая проверка здоровья системы"""
    
    print("🏥 ПРОВЕРКА ЗДОРОВЬЯ СИСТЕМЫ")
    print("=" * 40)
    print(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    checks = []
    
    # 1. Проверка подключения к БД
    print("1️⃣ Проверка подключения к базе данных...")
    try:
        from database import db_manager
        conn = db_manager.get_connection()
        if conn and not conn.closed:
            checks.append(("База данных", True, "✅ Подключение успешно"))
        else:
            checks.append(("База данных", False, "❌ Нет подключения"))
    except Exception as e:
        checks.append(("База данных", False, f"❌ Ошибка: {e}"))
    
    # 2. Проверка импорта модулей аналитики
    print("2️⃣ Проверка модулей аналитики...")
    try:
        sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
        from analytics.transaction_analyzer import TransactionAnalyzer
        from analytics.transfer_analyzer import TransferAnalyzer
        from analytics.pattern_detector import PatternDetector
        checks.append(("Модули аналитики", True, "✅ Все модули загружены"))
    except Exception as e:
        checks.append(("Модули аналитики", False, f"❌ Ошибка: {e}"))
    
    # 3. Проверка утилит
    print("3️⃣ Проверка утилит...")
    try:
        from utils.date_utils import DateUtils
        from utils.math_utils import MathUtils
        checks.append(("Утилиты", True, "✅ Утилиты загружены"))
    except Exception as e:
        checks.append(("Утилиты", False, f"❌ Ошибка: {e}"))
    
    # 4. Проверка доступа к данным
    print("4️⃣ Проверка доступа к данным...")
    try:
        clients = db_manager.get_clients(limit=1)
        if clients:
            checks.append(("Доступ к данным", True, f"✅ Найдено {len(clients)} клиентов"))
        else:
            checks.append(("Доступ к данным", False, "❌ Нет данных"))
    except Exception as e:
        checks.append(("Доступ к данным", False, f"❌ Ошибка: {e}"))
    
    # Выводим результаты
    print()
    print("📊 РЕЗУЛЬТАТЫ ПРОВЕРКИ")
    print("-" * 40)
    
    all_passed = True
    for name, status, message in checks:
        print(f"{message}")
        if not status:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 СИСТЕМА ГОТОВА К РАБОТЕ!")
        return True
    else:
        print("⚠️  ОБНАРУЖЕНЫ ПРОБЛЕМЫ!")
        return False


def main():
    """Основная функция"""
    success = health_check()
    
    if success:
        print("✅ Проверка здоровья завершена успешно")
        sys.exit(0)
    else:
        print("❌ Проверка здоровья выявила проблемы")
        sys.exit(1)


if __name__ == '__main__':
    main()
