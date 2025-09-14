"""
Слой уведомлений и прокси-ИИ для генерации персонализированных сообщений
"""

from .notification_ai import NotificationAI
from .message_templates import MessageTemplates
from .notification_generator import NotificationGenerator
from .scenario_integration import ScenarioIntegration

__all__ = ['NotificationAI', 'MessageTemplates', 'NotificationGenerator', 'ScenarioIntegration']
