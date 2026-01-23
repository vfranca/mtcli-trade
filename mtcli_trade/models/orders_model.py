"""
Modelo de normalização de ordens pendentes.
"""

import MetaTrader5 as mt5
from mtcli_trade.conf import DIGITOS


ORDER_TYPE_MAP = {
    mt5.ORDER_TYPE_BUY_LIMIT: "BUY_LIMIT",
    mt5.ORDER_TYPE_SELL_LIMIT: "SELL_LIMIT",
    mt5.ORDER_TYPE_BUY_STOP: "BUY_STOP",
    mt5.ORDER_TYPE_SELL_STOP: "SELL_STOP",
}


def normalizar_ordem(ordem):
    """
    Converte uma ordem MT5 em estrutura simples para CLI/View.
    """
    return {
        "tipo": ORDER_TYPE_MAP.get(ordem.type, f"TYPE_{ordem.type}"),
        "symbol": ordem.symbol,
        "volume": ordem.volume_current,
        "preco": round(ordem.price_open, DIGITOS),
        "ticket": ordem.ticket,
    }
