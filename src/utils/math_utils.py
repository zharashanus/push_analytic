"""
Математические утилиты
"""

from typing import List, Dict, Any, Union
import statistics


class MathUtils:
    """Утилиты для математических вычислений"""
    
    @staticmethod
    def calculate_percentage(part: float, whole: float) -> float:
        """
        Рассчитать процент
        
        Args:
            part: Часть
            whole: Целое
        
        Returns:
            Процент
        """
        if whole == 0:
            return 0
        return (part / whole) * 100
    
    @staticmethod
    def calculate_growth_rate(old_value: float, new_value: float) -> float:
        """
        Рассчитать темп роста
        
        Args:
            old_value: Старое значение
            new_value: Новое значение
        
        Returns:
            Темп роста в процентах
        """
        if old_value == 0:
            return 0
        return ((new_value - old_value) / old_value) * 100
    
    @staticmethod
    def calculate_average(values: List[float]) -> float:
        """
        Рассчитать среднее значение
        
        Args:
            values: Список значений
        
        Returns:
            Среднее значение
        """
        if not values:
            return 0
        return statistics.mean(values)
    
    @staticmethod
    def calculate_median(values: List[float]) -> float:
        """
        Рассчитать медиану
        
        Args:
            values: Список значений
        
        Returns:
            Медиана
        """
        if not values:
            return 0
        return statistics.median(values)
    
    @staticmethod
    def calculate_standard_deviation(values: List[float]) -> float:
        """
        Рассчитать стандартное отклонение
        
        Args:
            values: Список значений
        
        Returns:
            Стандартное отклонение
        """
        if len(values) < 2:
            return 0
        return statistics.stdev(values)
    
    @staticmethod
    def calculate_variance(values: List[float]) -> float:
        """
        Рассчитать дисперсию
        
        Args:
            values: Список значений
        
        Returns:
            Дисперсия
        """
        if len(values) < 2:
            return 0
        return statistics.variance(values)
    
    @staticmethod
    def calculate_percentile(values: List[float], percentile: float) -> float:
        """
        Рассчитать перцентиль
        
        Args:
            values: Список значений
            percentile: Перцентиль (0-100)
        
        Returns:
            Значение перцентиля
        """
        if not values:
            return 0
        
        sorted_values = sorted(values)
        index = (percentile / 100) * (len(sorted_values) - 1)
        
        if index.is_integer():
            return sorted_values[int(index)]
        else:
            lower = sorted_values[int(index)]
            upper = sorted_values[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))
    
    @staticmethod
    def calculate_correlation(x_values: List[float], y_values: List[float]) -> float:
        """
        Рассчитать корреляцию Пирсона
        
        Args:
            x_values: Значения X
            y_values: Значения Y
        
        Returns:
            Коэффициент корреляции
        """
        if len(x_values) != len(y_values) or len(x_values) < 2:
            return 0
        
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        sum_y2 = sum(y * y for y in y_values)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2)) ** 0.5
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    
    @staticmethod
    def calculate_trend(values: List[float]) -> str:
        """
        Определить тренд в данных
        
        Args:
            values: Список значений
        
        Returns:
            'increasing', 'decreasing', 'stable'
        """
        if len(values) < 2:
            return 'stable'
        
        # Простой линейный тренд
        x = list(range(len(values)))
        n = len(x)
        
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(xi**2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
        
        if slope > 0.1:
            return 'increasing'
        elif slope < -0.1:
            return 'decreasing'
        else:
            return 'stable'
    
    @staticmethod
    def calculate_volatility(values: List[float]) -> float:
        """
        Рассчитать волатильность (коэффициент вариации)
        
        Args:
            values: Список значений
        
        Returns:
            Коэффициент вариации
        """
        if not values:
            return 0
        
        mean_value = MathUtils.calculate_average(values)
        if mean_value == 0:
            return 0
        
        std_dev = MathUtils.calculate_standard_deviation(values)
        return (std_dev / mean_value) * 100
    
    @staticmethod
    def normalize_value(value: float, min_val: float, max_val: float) -> float:
        """
        Нормализовать значение в диапазоне 0-1
        
        Args:
            value: Значение для нормализации
            min_val: Минимальное значение
            max_val: Максимальное значение
        
        Returns:
            Нормализованное значение
        """
        if max_val == min_val:
            return 0
        
        return (value - min_val) / (max_val - min_val)
    
    @staticmethod
    def calculate_weighted_average(values: List[float], weights: List[float]) -> float:
        """
        Рассчитать взвешенное среднее
        
        Args:
            values: Список значений
            weights: Список весов
        
        Returns:
            Взвешенное среднее
        """
        if len(values) != len(weights) or not values:
            return 0
        
        weighted_sum = sum(v * w for v, w in zip(values, weights))
        total_weight = sum(weights)
        
        if total_weight == 0:
            return 0
        
        return weighted_sum / total_weight
    
    @staticmethod
    def calculate_compound_growth_rate(initial_value: float, final_value: float, periods: int) -> float:
        """
        Рассчитать сложный темп роста
        
        Args:
            initial_value: Начальное значение
            final_value: Конечное значение
            periods: Количество периодов
        
        Returns:
            Сложный темп роста в процентах
        """
        if initial_value <= 0 or periods <= 0:
            return 0
        
        growth_rate = (final_value / initial_value) ** (1 / periods) - 1
        return growth_rate * 100
    
    @staticmethod
    def round_to_nearest(value: float, nearest: float) -> float:
        """
        Округлить до ближайшего значения
        
        Args:
            value: Значение для округления
            nearest: Шаг округления
        
        Returns:
            Округленное значение
        """
        return round(value / nearest) * nearest
