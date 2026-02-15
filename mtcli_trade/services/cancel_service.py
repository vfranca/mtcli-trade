"""
Serviço responsável por cancelar ordens pendentes.
"""

import MetaTrader5 as mt5
from .mt5_service import MT5Service

mt5_service = MT5Service()


def cancelar_ordem_mt5(ticket: int):
    """
    Cancela ordem pendente pelo ticket.

    :param ticket: número do ticket
    :return: OrderSendResult
    """

    request = {
        "action": mt5.TRADE_ACTION_REMOVE,
        "order": ticket,
        "comment": "mtcli-trade cancel",
    }

    return mt5_service.enviar_request(request)
