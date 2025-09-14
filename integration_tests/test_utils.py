"""
Тест утилит
"""

import sys
import os
import unittest
from datetime import datetime, timedelta

# Добавляем путь к src для импорта модулей
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from utils.date_utils import DateUtils
from utils.math_utils import MathUtils


class TestUtils(unittest.TestCase):
    """Тесты утилит"""
    
    def test_date_utils(self):
        """Тест утилит для работы с датами"""
        print("📅 Тестирование утилит для дат...")
        
        # Тест получения диапазона дат
        start_date, end_date = DateUtils.get_date_range(30)
        self.assertIsInstance(start_date, datetime)
        self.assertIsInstance(end_date, datetime)
        self.assertLess(start_date, end_date)
        print("   ✅ Получение диапазона дат работает")
        
        # Тест форматирования даты
        test_date = datetime(2024, 1, 15)
        formatted = DateUtils.format_date(test_date)
        self.assertEqual(formatted, "2024-01-15")
        print("   ✅ Форматирование даты работает")
        
        # Тест парсинга даты
        parsed_date = DateUtils.parse_date("2024-01-15")
        self.assertEqual(parsed_date, test_date)
        print("   ✅ Парсинг даты работает")
        
        # Тест проверки выходных
        monday = datetime(2024, 1, 15)  # Понедельник
        saturday = datetime(2024, 1, 20)  # Суббота
        
        self.assertFalse(DateUtils.is_weekend(monday))
        self.assertTrue(DateUtils.is_weekend(saturday))
        print("   ✅ Проверка выходных работает")
        
        # Тест получения месячных периодов
        periods = DateUtils.get_month_periods(90)
        self.assertIsInstance(periods, list)
        self.assertGreater(len(periods), 0)
        print(f"   ✅ Получено {len(periods)} месячных периодов")
        
        # Тест подсчета рабочих дней
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 7)
        business_days = DateUtils.get_business_days_count(start, end)
        self.assertGreater(business_days, 0)
        print(f"   ✅ Рабочих дней в периоде: {business_days}")
    
    def test_math_utils(self):
        """Тест математических утилит"""
        print("🧮 Тестирование математических утилит...")
        
        # Тест расчета процента
        percentage = MathUtils.calculate_percentage(25, 100)
        self.assertEqual(percentage, 25.0)
        print("   ✅ Расчет процента работает")
        
        # Тест расчета темпа роста
        growth_rate = MathUtils.calculate_growth_rate(100, 120)
        self.assertEqual(growth_rate, 20.0)
        print("   ✅ Расчет темпа роста работает")
        
        # Тест расчета среднего
        values = [1, 2, 3, 4, 5]
        average = MathUtils.calculate_average(values)
        self.assertEqual(average, 3.0)
        print("   ✅ Расчет среднего работает")
        
        # Тест расчета медианы
        median = MathUtils.calculate_median(values)
        self.assertEqual(median, 3.0)
        print("   ✅ Расчет медианы работает")
        
        # Тест расчета стандартного отклонения
        std_dev = MathUtils.calculate_standard_deviation(values)
        self.assertGreater(std_dev, 0)
        print(f"   ✅ Стандартное отклонение: {std_dev:.2f}")
        
        # Тест расчета перцентиля
        percentile_50 = MathUtils.calculate_percentile(values, 50)
        self.assertEqual(percentile_50, 3.0)
        print("   ✅ Расчет перцентиля работает")
        
        # Тест расчета корреляции
        x_values = [1, 2, 3, 4, 5]
        y_values = [2, 4, 6, 8, 10]
        correlation = MathUtils.calculate_correlation(x_values, y_values)
        self.assertAlmostEqual(correlation, 1.0, places=5)
        print(f"   ✅ Корреляция: {correlation:.2f}")
        
        # Тест определения тренда
        increasing_values = [1, 2, 3, 4, 5]
        decreasing_values = [5, 4, 3, 2, 1]
        stable_values = [3, 3, 3, 3, 3]
        
        self.assertEqual(MathUtils.calculate_trend(increasing_values), 'increasing')
        self.assertEqual(MathUtils.calculate_trend(decreasing_values), 'decreasing')
        self.assertEqual(MathUtils.calculate_trend(stable_values), 'stable')
        print("   ✅ Определение тренда работает")
        
        # Тест расчета волатильности
        volatile_values = [1, 10, 2, 9, 3, 8]
        volatility = MathUtils.calculate_volatility(volatile_values)
        self.assertGreater(volatility, 0)
        print(f"   ✅ Волатильность: {volatility:.2f}%")
        
        # Тест нормализации
        normalized = MathUtils.normalize_value(5, 0, 10)
        self.assertEqual(normalized, 0.5)
        print("   ✅ Нормализация работает")
        
        # Тест взвешенного среднего
        weights = [0.1, 0.2, 0.3, 0.4]
        weighted_avg = MathUtils.calculate_weighted_average(values, weights)
        self.assertGreaterEqual(weighted_avg, 0)
        print(f"   ✅ Взвешенное среднее: {weighted_avg:.2f}")
        
        # Тест сложного темпа роста
        cgr = MathUtils.calculate_compound_growth_rate(100, 121, 2)
        self.assertAlmostEqual(cgr, 10.0, places=1)
        print(f"   ✅ Сложный темп роста: {cgr:.2f}%")
        
        # Тест округления
        rounded = MathUtils.round_to_nearest(23, 5)
        self.assertEqual(rounded, 25)
        print("   ✅ Округление работает")


if __name__ == '__main__':
    print("🚀 Запуск тестов утилит...")
    unittest.main(verbosity=2)
