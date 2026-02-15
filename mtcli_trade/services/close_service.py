"""
Serviço responsável pelo fechamento de posições no MT5.
"""

import MetaTrader5 as mt5
from mtcli.conecta import conectar, shutdown


def fechar_posicao_mt5(posicao):
    """
    Fecha uma posição individual.

    :param posicao: objeto retornado por mt5.positions_get
    :return: resultado do order_send
    """

    conectar()
    try:
        tick = mt5.symbol_info_tick(posicao.symbol)

        if not tick:
            return None

        # Define lado oposto
        if posicao.type == mt5.POSITION_TYPE_BUY:
            tipo_ordem = mt5.ORDER_TYPE_SELL
            preco = tick.bid
        else:
            tipo_ordem = mt5.ORDER_TYPE_BUY
            preco = tick.ask

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": posicao.symbol,
            "volume": posicao.volume,
            "type": tipo_ordem,
            "position": posicao.ticket,
            "price": preco,
            "deviation": 20,
            "magic": 123456,
            "comment": "MT CLI Close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        return mt5.order_send(request)

    finally:
        shutdown()
