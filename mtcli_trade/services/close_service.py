"""
Serviço responsável pelo fechamento de posições.
"""

import MetaTrader5 as mt5
from .mt5_service import MT5Service

mt5_service = MT5Service()


def fechar_posicao_mt5(symbol: str, ticket: int, volume: float, tipo_posicao: int):
    """
    Fecha uma posição específica.

    :param symbol: ativo
    :param ticket: ticket da posição
    :param volume: volume da posição
    :param tipo_posicao: mt5.POSITION_TYPE_*
    :return: OrderSendResult
    """

    tick = mt5_service.obter_tick(symbol)

    if tipo_posicao == mt5.POSITION_TYPE_BUY:
        tipo_ordem = mt5.ORDER_TYPE_SELL
        preco = tick.bid
    else:
        tipo_ordem = mt5.ORDER_TYPE_BUY
        preco = tick.ask

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": tipo_ordem,
        "position": ticket,
        "price": preco,
        "deviation": 20,
        "magic": 123456,
        "comment": "mtcli-trade close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    return mt5_service.enviar_request(request)
