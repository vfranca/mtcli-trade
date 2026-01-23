"""
Serviços de integração com o MetaTrader 5 (MT5).

Este módulo é a ÚNICA camada autorizada a:
- Conectar/desconectar do MT5
- Enviar ordens
- Cancelar ordens
- Obter ticks e informações de mercado

Controllers e models nunca devem acessar o MT5 diretamente.
"""

import MetaTrader5 as mt5
from mtcli.conecta import conectar, shutdown
from mtcli.logger import setup_logger

log = setup_logger()


# ==========================================================
# UTILIDADES BÁSICAS
# ==========================================================

def _conectar():
    """
    Garante conexão com o MT5.
    """
    if not mt5.initialize():
        conectar()


def _desconectar():
    """
    Encerra a conexão com o MT5.
    """
    shutdown()


# ==========================================================
# MERCADO / COTAÇÃO
# ==========================================================

def obter_tick(symbol):
    """
    Retorna o tick atual de um símbolo.

    :param symbol: Ativo (ex: WIN, WDO, PETR4)
    :return: mt5.Tick
    :raises RuntimeError: se não for possível obter o tick
    """
    _conectar()
    try:
        if not mt5.symbol_select(symbol, True):
            raise RuntimeError(f"Erro ao selecionar símbolo {symbol}")

        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            raise RuntimeError(f"Erro ao obter tick de {symbol}")

        return tick
    finally:
        _desconectar()


# ==========================================================
# ENVIO DE ORDENS
# ==========================================================

def enviar_ordem_mt5(ordem):
    """
    Envia uma ordem ao MT5.

    :param ordem: dict compatível com mt5.order_send
    :return: resultado do MT5
    :raises RuntimeError: em caso de falha
    """
    _conectar()
    try:
        log.debug(f"Enviando ordem MT5: {ordem}")
        resultado = mt5.order_send(ordem)

        if resultado.retcode not in (
            mt5.TRADE_RETCODE_DONE,
            mt5.TRADE_RETCODE_PLACED,
        ):
            raise RuntimeError(
                f"Falha no envio da ordem "
                f"(retcode={resultado.retcode}, comment={resultado.comment})"
            )

        log.info(
            f"Ordem enviada com sucesso | ticket={resultado.order} | retcode={resultado.retcode}"
        )
        return resultado
    finally:
        _desconectar()


# ==========================================================
# CANCELAMENTO DE ORDENS
# ==========================================================

def cancelar_ordem_mt5(ordem):
    """
    Cancela uma ordem pendente específica.

    :param ordem: objeto retornado por mt5.orders_get
    :return: resultado do MT5
    :raises RuntimeError: se falhar
    """
    _conectar()
    try:
        req = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": ordem.ticket,
            "symbol": ordem.symbol,
            "magic": 1000,
            "comment": "mtcli-trade cancel",
        }

        log.debug(f"Cancelando ordem MT5: {req}")
        resultado = mt5.order_send(req)

        if resultado.retcode != mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(
                f"Erro ao cancelar ordem {ordem.ticket} "
                f"(retcode={resultado.retcode})"
            )

        log.info(f"Ordem cancelada com sucesso | ticket={ordem.ticket}")
        return resultado
    finally:
        _desconectar()


# ==========================================================
# FECHAMENTO DE POSIÇÕES
# ==========================================================

def fechar_posicao_mt5(posicao):
    """
    Fecha uma posição aberta.

    :param posicao: objeto retornado por mt5.positions_get
    :return: resultado do MT5
    """
    _conectar()
    try:
        tick = mt5.symbol_info_tick(posicao.symbol)
        if not tick:
            raise RuntimeError(f"Erro ao obter tick para {posicao.symbol}")

        ordem = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": posicao.symbol,
            "volume": posicao.volume,
            "type": (
                mt5.ORDER_TYPE_SELL
                if posicao.type == mt5.POSITION_TYPE_BUY
                else mt5.ORDER_TYPE_BUY
            ),
            "price": (
                tick.bid
                if posicao.type == mt5.POSITION_TYPE_BUY
                else tick.ask
            ),
            "deviation": 10,
            "magic": 1001,
            "comment": "mtcli-trade zera",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        log.debug(f"Fechando posição MT5: {ordem}")
        resultado = mt5.order_send(ordem)

        if resultado.retcode != mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(
                f"Erro ao fechar posição {posicao.ticket} "
                f"(retcode={resultado.retcode})"
            )

        log.info(
            f"Posição encerrada | ticket={posicao.ticket} | symbol={posicao.symbol}"
        )
        return resultado
    finally:
        _desconectar()
