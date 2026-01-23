"""
Modelo de normalização de posições abertas.

Este módulo NÃO executa ações no MetaTrader 5.
Ele apenas converte objetos retornados pelo MT5
em estruturas simples, adequadas para controllers e views.
"""

import MetaTrader5 as mt5
from mtcli_trade.conf import DIGITOS


def normalizar_posicao(posicao):
    """
    Converte uma posição MT5 em um dicionário simples.

    :param posicao: objeto retornado por mt5.positions_get
    :return: dict normalizado
    """
    return {
        "ticket": posicao.ticket,
        "symbol": posicao.symbol,
        "tipo": _tipo_posicao(posicao.type),
        "volume": round(posicao.volume, 2),
        "preco_abertura": round(posicao.price_open, DIGITOS),
        "lucro": round(posicao.profit, 2),
        "swap": round(posicao.swap, 2),
    }


def _tipo_posicao(tipo_mt5):
    """
    Traduz o tipo da posição MT5 para texto legível.

    :param tipo_mt5: constante mt5.POSITION_TYPE_*
    :return: str
    """
    if tipo_mt5 == mt5.POSITION_TYPE_BUY:
        return "BUY"
    if tipo_mt5 == mt5.POSITION_TYPE_SELL:
        return "SELL"
    return f"TYPE_{tipo_mt5}"
