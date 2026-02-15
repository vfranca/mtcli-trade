"""
Factory responsável por criar controllers de ordem.

Remove duplicação entre BUY e SELL.
Centraliza configuração dos tipos MT5.
"""

import MetaTrader5 as mt5
from .order_controller import OrderController


class OrderFactory:
    """
    Factory para criação de controllers de ordem.
    """

    @staticmethod
    def create(side: str) -> OrderController:
        """
        Cria controller baseado no lado da operação.

        Args:
            side (str): "buy" ou "sell"

        Returns:
            OrderController

        Raises:
            ValueError: se lado inválido.
        """

        side = side.lower()

        if side == "buy":
            return OrderController(
                order_type_market=mt5.ORDER_TYPE_BUY,
                order_type_limit=mt5.ORDER_TYPE_BUY_LIMIT,
                order_type_stop=mt5.ORDER_TYPE_BUY_STOP,
                price_from_tick="ask",
            )

        if side == "sell":
            return OrderController(
                order_type_market=mt5.ORDER_TYPE_SELL,
                order_type_limit=mt5.ORDER_TYPE_SELL_LIMIT,
                order_type_stop=mt5.ORDER_TYPE_SELL_STOP,
                price_from_tick="bid",
            )

        raise ValueError(f"Lado inválido para ordem: {side}")
