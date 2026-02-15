"""
Camada de serviço responsável pela integração com MetaTrader 5.

REGRAS ARQUITETURAIS:
- Esta é a única camada autorizada a acessar mt5.*
- Controllers e Models NÃO devem importar MetaTrader5 diretamente.
- Cada operação abre e fecha conexão de forma segura.
- Todas as falhas são convertidas em RuntimeError.

Responsabilidades:
- Conectar / desconectar do MT5
- Obter ticks
- Enviar ordens
- Cancelar ordens
- Fechar posições
"""

import MetaTrader5 as mt5
from mtcli.conecta import conectar, shutdown
from mtcli.logger import setup_logger

log = setup_logger()


# ==========================================================
# CONTROLE DE CONEXÃO
# ==========================================================

def _conectar():
    """
    Garante conexão ativa com o MetaTrader 5.

    Raises:
        RuntimeError: se não for possível conectar.
    """
    if not mt5.initialize():
        log.debug("MT5 não inicializado. Tentando conectar via mtcli.")
        if not conectar():
            raise RuntimeError("Falha ao conectar ao MetaTrader 5")


def _desconectar():
    """
    Encerra conexão com o MT5 de forma segura.
    """
    shutdown()


# ==========================================================
# MERCADO / COTAÇÃO
# ==========================================================

def obter_tick(symbol):
    """
    Retorna o tick atual de um símbolo.

    Args:
        symbol (str): Código do ativo.

    Returns:
        mt5.Tick: Objeto contendo bid/ask.

    Raises:
        RuntimeError: se não for possível obter tick.
    """
    _conectar()
    try:
        if not mt5.symbol_select(symbol, True):
            raise RuntimeError(f"Erro ao selecionar símbolo {symbol}")

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            raise RuntimeError(f"Erro ao obter tick de {symbol}")

        return tick

    finally:
        _desconectar()


# ==========================================================
# ENVIO DE ORDENS
# ==========================================================

def enviar_ordem_mt5(ordem):
    """
    Envia uma ordem ao MetaTrader 5.

    Args:
        ordem (dict): Payload compatível com mt5.order_send.

    Returns:
        mt5.OrderSendResult

    Raises:
        RuntimeError: em caso de falha operacional.
    """
    _conectar()
    try:
        log.debug(f"Enviando ordem MT5: {ordem}")

        resultado = mt5.order_send(ordem)

        if resultado is None:
            raise RuntimeError("MetaTrader 5 não retornou resposta ao enviar ordem")

        if resultado.retcode not in (
            mt5.TRADE_RETCODE_DONE,
            mt5.TRADE_RETCODE_PLACED,
        ):
            raise RuntimeError(
                f"Falha no envio da ordem "
                f"(retcode={resultado.retcode}, comment={resultado.comment})"
            )

        log.info(
            f"Ordem enviada com sucesso | "
            f"ticket={resultado.order} | "
            f"retcode={resultado.retcode}"
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

    Args:
        ordem: Objeto retornado por mt5.orders_get.

    Returns:
        mt5.OrderSendResult

    Raises:
        RuntimeError: se falhar.
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

        if resultado is None:
            raise RuntimeError("MetaTrader 5 não retornou resposta ao cancelar ordem")

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

    Args:
        posicao: Objeto retornado por mt5.positions_get.

    Returns:
        mt5.OrderSendResult

    Raises:
        RuntimeError: se falhar.
    """
    _conectar()
    try:
        tick = mt5.symbol_info_tick(posicao.symbol)

        if tick is None:
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

        if resultado is None:
            raise RuntimeError("MetaTrader 5 não retornou resposta ao fechar posição")

        if resultado.retcode != mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(
                f"Erro ao fechar posição {posicao.ticket} "
                f"(retcode={resultado.retcode})"
            )

        log.info(
            f"Posição encerrada | "
            f"ticket={posicao.ticket} | "
            f"symbol={posicao.symbol}"
        )

        return resultado

    finally:
        _desconectar()
