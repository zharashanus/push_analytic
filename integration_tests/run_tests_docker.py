"""
Запуск тестов в Docker контейнере
"""

import subprocess
import sys
import os
from datetime import datetime

def run_tests_in_docker():
    """Запуск тестов в Docker"""
    
    print("🐳 ЗАПУСК ТЕСТОВ В DOCKER")
    print("=" * 40)
    print(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Команды для запуска тестов
    commands = [
        # Быстрая проверка здоровья
        "python integration_tests/health_check.py",
        
        # Полные интеграционные тесты
        "python integration_tests/run_all_tests.py"
    ]
    
    for i, command in enumerate(commands, 1):
        print(f"{i}️⃣ Выполнение: {command}")
        print("-" * 30)
        
        try:
            # Запускаем команду
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 минут таймаут
            )
            
            # Выводим результат
            if result.stdout:
                print(result.stdout)
            
            if result.stderr:
                print("STDERR:", result.stderr)
            
            if result.returncode == 0:
                print("✅ Команда выполнена успешно")
            else:
                print(f"❌ Команда завершилась с ошибкой (код: {result.returncode})")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Команда превысила время ожидания")
            return False
        except Exception as e:
            print(f"❌ Ошибка при выполнении команды: {e}")
            return False
        
        print()
    
    print("🎉 ВСЕ ТЕСТЫ В DOCKER ВЫПОЛНЕНЫ УСПЕШНО!")
    return True


def main():
    """Основная функция"""
    success = run_tests_in_docker()
    
    if success:
        print("✅ Тесты в Docker завершены успешно")
        sys.exit(0)
    else:
        print("❌ Тесты в Docker завершились с ошибками")
        sys.exit(1)


if __name__ == '__main__':
    main()
