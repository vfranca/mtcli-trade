"""
Serviço de infraestrutura MT5.

IMPORTANTE:
- Não gerencia conexão.
- Depende de mt5_conexao do mtcli.
- Não contém lógica de negócio.
"""

import MetaTrader5 as mt5
from mtcli.logger import setup_logger

log = setup_logger()


class MT5Service:
    """
    Camada de acesso direto ao MetaTrader 5.
    """

    # ======================================================
    # CONSULTAS
    # ======================================================

    def obter_tick(self, symbol: str):
        if not mt5.symbol_select(symbol, True):
            raise RuntimeError(f"Erro ao selecionar símbolo {symbol}")

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            raise RuntimeError(f"Erro ao obter tick de {symbol}")

        return tick

    def obter_ordens(self, symbol: str | None = None):
        return (
            mt5.orders_get(symbol=symbol)
            if symbol
            else mt5.orders_get()
        )

    def obter_posicoes(self, symbol: str | None = None):
        return (
            mt5.positions_get(symbol=symbol)
            if symbol
            else mt5.positions_get()
        )

    # ======================================================
    # EXECUÇÃO
    # ======================================================

    def enviar_request(self, request: dict):
        log.debug(f"Enviando request MT5: {request}")

        resultado = mt5.order_send(request)

        if resultado is None:
            raise RuntimeError("MetaTrader 5 não retornou resposta")

        if resultado.retcode not in (
            mt5.TRADE_RETCODE_DONE,
            mt5.TRADE_RETCODE_PLACED,
        ):
            raise RuntimeError(
                f"Erro MT5 (retcode={resultado.retcode}, "
                f"comment={resultado.comment})"
            )

        log.info(f"Request executado | retcode={resultado.retcode}")

        return resultado
