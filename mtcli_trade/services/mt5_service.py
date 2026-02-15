"""
Serviço central de integração com MetaTrader 5.

REGRAS:
- ÚNICA camada autorizada a acessar MetaTrader5.
- Não contém lógica de negócio.
- Não recebe objetos MT5 externos.
- Controllers não devem importar MetaTrader5.
- Sempre garante conexão segura.
"""

import MetaTrader5 as mt5
from mtcli.conecta import conectar, shutdown
from mtcli.logger import setup_logger

log = setup_logger()


class MT5Service:
    """
    Serviço de infraestrutura para comunicação com MT5.
    """

    # ======================================================
    # CONTROLE DE CONEXÃO
    # ======================================================

    def _conectar(self):
        if not mt5.initialize():
            log.debug("MT5 não inicializado. Tentando conectar via mtcli.")
            if not conectar():
                raise RuntimeError("Falha ao conectar ao MetaTrader 5")

    def _desconectar(self):
        shutdown()

    # ======================================================
    # CONSULTAS
    # ======================================================

    def obter_tick(self, symbol: str):
        """
        Retorna tick atual.
        """
        self._conectar()
        try:
            if not mt5.symbol_select(symbol, True):
                raise RuntimeError(f"Erro ao selecionar símbolo {symbol}")

            tick = mt5.symbol_info_tick(symbol)

            if tick is None:
                raise RuntimeError(f"Erro ao obter tick de {symbol}")

            return tick

        finally:
            self._desconectar()

    def obter_ordens(self, symbol: str | None = None):
        """
        Retorna ordens pendentes.
        """
        self._conectar()
        try:
            return (
                mt5.orders_get(symbol=symbol)
                if symbol
                else mt5.orders_get()
            )
        finally:
            self._desconectar()

    def obter_posicoes(self, symbol: str | None = None):
        """
        Retorna posições abertas.
        """
        self._conectar()
        try:
            return (
                mt5.positions_get(symbol=symbol)
                if symbol
                else mt5.positions_get()
            )
        finally:
            self._desconectar()

    # ======================================================
    # EXECUÇÃO
    # ======================================================

    def enviar_request(self, request: dict):
        """
        Envia request genérico ao MT5.

        :param request: dicionário compatível com order_send
        :return: OrderSendResult
        """
        self._conectar()
        try:
            log.debug(f"Enviando request MT5: {request}")

            resultado = mt5.order_send(request)

            if resultado is None:
                raise RuntimeError(
                    "MetaTrader 5 não retornou resposta"
                )

            if resultado.retcode not in (
                mt5.TRADE_RETCODE_DONE,
                mt5.TRADE_RETCODE_PLACED,
            ):
                raise RuntimeError(
                    f"Erro MT5 (retcode={resultado.retcode}, "
                    f"comment={resultado.comment})"
                )

            log.info(
                f"Request executado com sucesso | "
                f"retcode={resultado.retcode}"
            )

            return resultado

        finally:
            self._desconectar()
