"""
Движок рекомендаций продуктов
"""

from typing import Dict, List, Any, Optional
from .product_matcher import ProductMatcher
from .scoring_engine import ScoringEngine


class RecommendationEngine:
    """Основной движок для генерации рекомендаций продуктов"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        self.product_matcher = ProductMatcher(db_manager)
        self.scoring_engine = ScoringEngine()
    
    def generate_recommendations(self, client_code: str, days: int = 90) -> Dict[str, Any]:
        """
        Генерация рекомендаций для клиента
        
        Args:
            client_code: Код клиента
            days: Период анализа в днях
        
        Returns:
            Словарь с рекомендациями
        """
        # Получаем информацию о клиенте
        client_info = self.db.get_client_by_code(client_code)
        if not client_info:
            return {'error': 'Клиент не найден'}
        
        # Получаем все доступные продукты
        all_products = self.db.get_products()
        if not all_products:
            return {'error': 'Продукты не найдены'}
        
        # Анализируем каждый продукт для клиента
        product_scores = []
        
        for product in all_products:
            # Получаем сценарий продукта
            product_scenario = self._get_product_scenario(product['name'])
            
            if product_scenario:
                # Анализируем соответствие клиента сценарию
                match_score = product_scenario.analyze_client(client_code, days, self.db)
                
                if match_score['score'] > 0:
                    product_scores.append({
                        'product': product,
                        'scenario': product_scenario,
                        'match_score': match_score,
                        'expected_benefit': match_score.get('expected_benefit', 0)
                    })
        
        # Сортируем по скору и выбираем топ-4
        product_scores.sort(key=lambda x: x['match_score']['score'], reverse=True)
        top_products = product_scores[:4]
        
        return {
            'client_code': client_code,
            'client_info': client_info,
            'recommendations': top_products,
            'total_analyzed': len(all_products),
            'total_matches': len(product_scores)
        }
    
    def _get_product_scenario(self, product_name: str):
        """Получить сценарий продукта по названию"""
        # Импортируем все сценарии продуктов
        from products.travel_card import TravelCardScenario
        from products.premium_card import PremiumCardScenario
        from products.credit_card import CreditCardScenario
        from products.currency_exchange import CurrencyExchangeScenario
        from products.cash_credit import CashCreditScenario
        from products.multi_currency_deposit import MultiCurrencyDepositScenario
        from products.savings_deposit import SavingsDepositScenario
        from products.accumulation_deposit import AccumulationDepositScenario
        from products.investments import InvestmentsScenario
        from products.gold_bars import GoldBarsScenario
        
        # Маппинг названий продуктов на сценарии
        scenarios = {
            'Карта для путешествий': TravelCardScenario(),
            'Премиальная карта': PremiumCardScenario(),
            'Кредитная карта': CreditCardScenario(),
            'Обмен валют': CurrencyExchangeScenario(),
            'Кредит наличными': CashCreditScenario(),
            'Депозит Мультивалютный': MultiCurrencyDepositScenario(),
            'Депозит Сберегательный': SavingsDepositScenario(),
            'Депозит Накопительный': AccumulationDepositScenario(),
            'Инвестиции': InvestmentsScenario(),
            'Золотые слитки': GoldBarsScenario()
        }
        
        return scenarios.get(product_name)
    
    def get_recommendation_summary(self, client_code: str, days: int = 90) -> Dict[str, Any]:
        """Получить краткую сводку рекомендаций"""
        recommendations = self.generate_recommendations(client_code, days)
        
        if 'error' in recommendations:
            return recommendations
        
        summary = {
            'client_code': client_code,
            'total_recommendations': len(recommendations['recommendations']),
            'top_recommendation': None,
            'categories': []
        }
        
        if recommendations['recommendations']:
            top_rec = recommendations['recommendations'][0]
            summary['top_recommendation'] = {
                'product_name': top_rec['product']['name'],
                'score': top_rec['match_score']['score'],
                'expected_benefit': top_rec['expected_benefit']
            }
            
            # Группируем по категориям
            categories = {}
            for rec in recommendations['recommendations']:
                category = rec['product'].get('category', 'other')
                if category not in categories:
                    categories[category] = []
                categories[category].append(rec['product']['name'])
            
            summary['categories'] = categories
        
        return summary
