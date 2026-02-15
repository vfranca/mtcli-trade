"""
Estratégia para ordem LIMIT.
"""

from .base_strategy import BaseOrderStrategy


class LimitStrategy(BaseOrderStrategy):

    def definir_tipo_ordem(self, controller):
        return controller.ORDER_TYPE_LIMIT

    def definir_preco(self, controller, tick, preco_input):
        if preco_input is None:
            raise ValueError("Preço é obrigatório para ordem LIMIT.")
        return preco_input
