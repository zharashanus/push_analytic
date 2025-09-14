"""
Запуск всех интеграционных тестов
Этот файл запускается при каждом запуске сервера
"""

import sys
import os
import unittest
import time
from datetime import datetime

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def run_all_tests():
    """Запуск всех интеграционных тестов"""
    
    print("🚀 ЗАПУСК ИНТЕГРАЦИОННЫХ ТЕСТОВ")
    print("=" * 50)
    print(f"⏰ Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Список всех тестовых модулей
    test_modules = [
        'integration_tests.test_database_connection',
        'integration_tests.test_utils',
        'integration_tests.test_analytics_layer'
    ]
    
    # Счетчики
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    skipped_tests = 0
    
    start_time = time.time()
    
    # Запускаем каждый модуль тестов
    for module_name in test_modules:
        print(f"📦 Запуск модуля: {module_name}")
        print("-" * 30)
        
        try:
            # Загружаем модуль
            module = __import__(module_name, fromlist=[''])
            
            # Создаем тестовый набор
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(module)
            
            # Запускаем тесты
            runner = unittest.TextTestRunner(
                verbosity=2,
                stream=sys.stdout,
                descriptions=True,
                failfast=False
            )
            
            result = runner.run(suite)
            
            # Подсчитываем результаты
            total_tests += result.testsRun
            passed_tests += result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
            failed_tests += len(result.failures) + len(result.errors)
            skipped_tests += len(result.skipped)
            
            print()
            
        except Exception as e:
            print(f"❌ Ошибка при запуске модуля {module_name}: {e}")
            failed_tests += 1
            print()
    
    # Выводим итоговую статистику
    end_time = time.time()
    duration = end_time - start_time
    
    print("=" * 50)
    print("📊 ИТОГОВАЯ СТАТИСТИКА")
    print("=" * 50)
    print(f"⏱️  Время выполнения: {duration:.2f} секунд")
    print(f"📈 Всего тестов: {total_tests}")
    print(f"✅ Пройдено: {passed_tests}")
    print(f"❌ Провалено: {failed_tests}")
    print(f"⏭️  Пропущено: {skipped_tests}")
    
    if failed_tests == 0:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        return True
    else:
        print("⚠️  НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ!")
        return False


def main():
    """Основная функция"""
    success = run_all_tests()
    
    # Возвращаем код выхода
    if success:
        sys.exit(0)  # Успех
    else:
        sys.exit(1)  # Ошибка


if __name__ == '__main__':
    main()
