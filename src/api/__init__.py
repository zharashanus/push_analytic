"""
API слой для REST эндпоинтов
"""

from .notification_api import app, analyze_client, analyze_client_all

__all__ = ['app', 'analyze_client', 'analyze_client_all']
