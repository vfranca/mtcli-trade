"""
Estratégia para ordem a mercado.
"""

from .base_strategy import BaseOrderStrategy


class MarketStrategy(BaseOrderStrategy):

    def definir_tipo_ordem(self, controller):
        return controller.ORDER_TYPE_MARKET

    def definir_preco(self, controller, tick, preco_input):
        return getattr(tick, controller.PRICE_FROM_TICK)
