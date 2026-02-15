"""
Estratégia para ordem STOP.
"""

from .base_strategy import BaseOrderStrategy


class StopStrategy(BaseOrderStrategy):

    def definir_tipo_ordem(self, controller):
        return controller.ORDER_TYPE_STOP

    def definir_preco(self, controller, tick, preco_input):
        if preco_input is None:
            raise ValueError("Preço é obrigatório para ordem STOP.")
        return preco_input
