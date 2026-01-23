"""
Controller base para envio de ordens (market, limit, stop).
Responsável por:
- Validação de flags
- Controle de risco
- Inicialização do símbolo
- Resolução do tipo de ordem
"""

import MetaTrader5 as mt5
from mtcli.logger import setup_logger
from ..models.ordem_model import criar_ordem
from ..models.risco_model import controlar_risco
from ..services.mt5_service import obter_tick, enviar_ordem_mt5
from ..conf import LOSS_LIMIT, STATUS_FILE

log = setup_logger()


class BaseOrderController:
    ORDER_TYPE_MARKET = None
    ORDER_TYPE_LIMIT = None
    ORDER_TYPE_STOP = None

    PRICE_FROM_TICK = None  # "ask" ou "bid"

    def executar(self, symbol, lot, sl, tp, limit, stop, preco):
        """
        Executa o fluxo completo de envio de ordem.

        :param symbol: Ativo
        :param lot: Volume
        :param sl: Stop loss (pontos)
        :param tp: Take profit (pontos)
        :param limit: Flag ordem limit
        :param stop: Flag ordem stop
        :param preco: Preço da ordem pendente
        """

        self._validar_flags(limit, stop)

        if controlar_risco(STATUS_FILE, LOSS_LIMIT):
            log.info("Envio bloqueado por risco")
            return

        tick = obter_tick(symbol)
        order_type, price, pending = self._resolver_tipo_ordem(
            tick, limit, stop, preco
        )

        ordem = criar_ordem(
            symbol=symbol,
            lot=lot,
            sl=sl,
            tp=tp,
            price=price,
            order_type=order_type,
            pending=pending,
        )

        enviar_ordem_mt5(ordem)

    @staticmethod
    def _validar_flags(limit, stop):
        if limit and stop:
            raise ValueError("Use apenas --limit OU --stop, nunca ambos.")

    def _resolver_tipo_ordem(self, tick, limit, stop, preco):
        if limit:
            if preco is None:
                raise ValueError("Ordens limit exigem --preco")
            return self.ORDER_TYPE_LIMIT, preco, True

        if stop:
            if preco is None:
                raise ValueError("Ordens stop exigem --preco")
            return self.ORDER_TYPE_STOP, preco, True

        price = getattr(tick, self.PRICE_FROM_TICK)
        return self.ORDER_TYPE_MARKET, price, False
