"""
Сценарии продуктов для анализа клиентов
"""

from .base_scenario_fixed import BaseProductScenario
from .accumulation_deposit import AccumulationDepositScenario
from .cash_credit import CashCreditScenario
from .credit_card import CreditCardScenario
from .currency_exchange import CurrencyExchangeScenario
from .gold_bars import GoldBarsScenario
from .investments import InvestmentsScenario
from .multi_currency_deposit import MultiCurrencyDepositScenario
from .premium_card import PremiumCardScenario
from .savings_deposit import SavingsDepositScenario
from .travel_card_fixed import TravelCardScenario

__all__ = [
    'BaseProductScenario',
    'AccumulationDepositScenario',
    'CashCreditScenario',
    'CreditCardScenario',
    'CurrencyExchangeScenario',
    'GoldBarsScenario',
    'InvestmentsScenario',
    'MultiCurrencyDepositScenario',
    'PremiumCardScenario',
    'SavingsDepositScenario',
    'TravelCardScenario'
]
