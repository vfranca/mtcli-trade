"""
Controller de ordens de compra.
"""

import MetaTrader5 as mt5
from .base_order_controller import BaseOrderController


class BuyController(BaseOrderController):
    ORDER_TYPE_MARKET = mt5.ORDER_TYPE_BUY
    ORDER_TYPE_LIMIT = mt5.ORDER_TYPE_BUY_LIMIT
    ORDER_TYPE_STOP = mt5.ORDER_TYPE_BUY_STOP
    PRICE_FROM_TICK = "ask"
