"""
Serviço responsável por cancelar ordens pendentes no MT5.
"""

import MetaTrader5 as mt5
from mtcli.conecta import conectar, shutdown


def cancelar_ordem_mt5(ticket: int):
    """
    Cancela uma ordem pendente pelo ticket.

    Args:
        ticket (int): Número do ticket da ordem.

    Returns:
        TradeResult
    """
    conectar()
    try:
        request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": ticket,
        }

        resultado = mt5.order_send(request)
        return resultado

    finally:
        shutdown()
