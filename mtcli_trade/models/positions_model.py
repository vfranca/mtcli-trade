"""
Modelo de normalização de posições abertas.

Este módulo NÃO executa ações no MetaTrader 5.
Ele apenas converte objetos retornados pelo MT5
em estruturas simples, adequadas para controllers e views.
"""

import MetaTrader5 as mt5
from mtcli_trade.conf import DIGITOS


# ---------------------------------------------------------
# Mapeamento de tipos de posição MT5
# ---------------------------------------------------------

POSITION_TYPE_MAP = {
    mt5.POSITION_TYPE_BUY: "BUY",
    mt5.POSITION_TYPE_SELL: "SELL",
}


# ---------------------------------------------------------
# Função principal de normalização
# ---------------------------------------------------------

def normalizar_posicao(posicao):
    """
    Converte uma posição MT5 em um dicionário simples.

    :param posicao: objeto retornado por mt5.positions_get
    :return: dict com dados normalizados
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


# ---------------------------------------------------------
# Funções auxiliares internas
# ---------------------------------------------------------

def _tipo_posicao(tipo_mt5):
    """
    Traduz o tipo da posição MT5 para texto legível.

    :param tipo_mt5: constante mt5.POSITION_TYPE_*
    :return: str
    """
    return POSITION_TYPE_MAP.get(tipo_mt5, f"TYPE_{tipo_mt5}")
