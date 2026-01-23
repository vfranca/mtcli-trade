"""
Controller de ordens de venda.
"""

import MetaTrader5 as mt5
from .base_order_controller import BaseOrderController


class SellController(BaseOrderController):
    ORDER_TYPE_MARKET = mt5.ORDER_TYPE_SELL
    ORDER_TYPE_LIMIT = mt5.ORDER_TYPE_SELL_LIMIT
    ORDER_TYPE_STOP = mt5.ORDER_TYPE_SELL_STOP
    PRICE_FROM_TICK = "bid"
