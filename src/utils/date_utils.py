"""
Утилиты для работы с датами
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any


class DateUtils:
    """Утилиты для работы с датами и временем"""
    
    @staticmethod
    def get_date_range(days: int) -> tuple:
        """
        Получить диапазон дат для анализа
        
        Args:
            days: Количество дней назад
        
        Returns:
            Кортеж (start_date, end_date)
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return start_date, end_date
    
    @staticmethod
    def format_date(date: datetime, format_str: str = '%Y-%m-%d') -> str:
        """
        Форматировать дату в строку
        
        Args:
            date: Дата для форматирования
            format_str: Формат строки
        
        Returns:
            Отформатированная дата
        """
        return date.strftime(format_str)
    
    @staticmethod
    def parse_date(date_str: str, format_str: str = '%Y-%m-%d') -> datetime:
        """
        Парсить дату из строки
        
        Args:
            date_str: Строка с датой
            format_str: Формат строки
        
        Returns:
            Объект datetime
        """
        return datetime.strptime(date_str, format_str)
    
    @staticmethod
    def is_weekend(date: datetime) -> bool:
        """
        Проверить, является ли дата выходным днем
        
        Args:
            date: Дата для проверки
        
        Returns:
            True если выходной
        """
        return date.weekday() >= 5  # 5 = суббота, 6 = воскресенье
    
    @staticmethod
    def get_month_periods(days: int) -> List[Dict[str, Any]]:
        """
        Получить список месячных периодов за указанное количество дней
        
        Args:
            days: Количество дней для анализа
        
        Returns:
            Список словарей с периодами
        """
        periods = []
        current_date = datetime.now()
        
        for i in range(days // 30 + 1):  # Примерно по месяцам
            month_start = current_date.replace(day=1) - timedelta(days=i * 30)
            month_end = month_start + timedelta(days=30)
            
            periods.append({
                'start': month_start,
                'end': month_end,
                'month_name': month_start.strftime('%B %Y')
            })
        
        return periods
    
    @staticmethod
    def get_week_periods(days: int) -> List[Dict[str, Any]]:
        """
        Получить список недельных периодов за указанное количество дней
        
        Args:
            days: Количество дней для анализа
        
        Returns:
            Список словарей с периодами
        """
        periods = []
        current_date = datetime.now()
        
        for i in range(days // 7 + 1):  # По неделям
            week_start = current_date - timedelta(days=i * 7)
            week_end = week_start + timedelta(days=7)
            
            periods.append({
                'start': week_start,
                'end': week_end,
                'week_number': i + 1
            })
        
        return periods
    
    @staticmethod
    def calculate_age_in_days(start_date: datetime, end_date: datetime) -> int:
        """
        Рассчитать возраст в днях
        
        Args:
            start_date: Начальная дата
            end_date: Конечная дата
        
        Returns:
            Количество дней
        """
        return (end_date - start_date).days
    
    @staticmethod
    def get_quarter(date: datetime) -> int:
        """
        Получить квартал для даты
        
        Args:
            date: Дата
        
        Returns:
            Номер квартала (1-4)
        """
        return (date.month - 1) // 3 + 1
    
    @staticmethod
    def is_business_day(date: datetime) -> bool:
        """
        Проверить, является ли дата рабочим днем
        
        Args:
            date: Дата для проверки
        
        Returns:
            True если рабочий день
        """
        return not DateUtils.is_weekend(date)
    
    @staticmethod
    def get_business_days_count(start_date: datetime, end_date: datetime) -> int:
        """
        Получить количество рабочих дней в периоде
        
        Args:
            start_date: Начальная дата
            end_date: Конечная дата
        
        Returns:
            Количество рабочих дней
        """
        current_date = start_date
        business_days = 0
        
        while current_date <= end_date:
            if DateUtils.is_business_day(current_date):
                business_days += 1
            current_date += timedelta(days=1)
        
        return business_days
