"""
Modelo de criação de ordens para MetaTrader5.
"""

import MetaTrader5 as mt5


def criar_ordem(symbol, lot, sl, tp, price, order_type, pending):
    """
    Cria o payload de ordem para mt5.order_send.

    :param symbol: Ativo
    :param lot: Volume
    :param sl: Stop loss em pontos
    :param tp: Take profit em pontos
    :param price: Preço da ordem
    :param order_type: Tipo MT5
    :param pending: True se ordem pendente
    """

    info = mt5.symbol_info(symbol)
    point = info.point if info else 0.01

    is_buy = order_type in (
        mt5.ORDER_TYPE_BUY,
        mt5.ORDER_TYPE_BUY_LIMIT,
        mt5.ORDER_TYPE_BUY_STOP,
    )

    sl_price = price - sl * point if is_buy else price + sl * point
    tp_price = price + tp * point if is_buy else price - tp * point

    return {
        "action": mt5.TRADE_ACTION_PENDING if pending else mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl_price,
        "tp": tp_price,
        "deviation": 10,
        "magic": 1000,
        "comment": "mtcli-trade",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
