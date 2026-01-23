"""
Modelo de normalização de posições abertas.
"""

import MetaTrader5 as mt5
from mtcli_trade.conf import DIGITOS


def normalizar_posicao(p):
    return {
        "symbol": p.symbol,
        "tipo": "BUY" if p.type == mt5.POSITION_TYPE_BUY else "SELL",
        "volume": round(p.volume, 2),
        "preco": round(p.price_open, DIGITOS),
        "lucro": round(p.profit, 2),
        "ticket": p.ticket,
    }
