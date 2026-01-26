"""
Controller base para envio de ordens (market, limit, stop).

Responsável por:
- Validação de flags
- Controle de risco
- Inicialização do símbolo
- Resolução do tipo de ordem
- Orquestração entre models e services
"""

import MetaTrader5 as mt5
from mtcli.logger import setup_logger
from ..models.ordem_model import criar_ordem
from ..models.risco_model import controlar_risco
from ..services.mt5_service import obter_tick, enviar_ordem_mt5
from ..conf import LOSS_LIMIT, STATUS_FILE

log = setup_logger()


class BaseOrderController:
    """
    Controller base para BUY e SELL.
    As subclasses devem definir:
    - ORDER_TYPE_MARKET
    - ORDER_TYPE_LIMIT
    - ORDER_TYPE_STOP
    - PRICE_FROM_TICK ("ask" ou "bid")
    """

    ORDER_TYPE_MARKET = None
    ORDER_TYPE_LIMIT = None
    ORDER_TYPE_STOP = None

    PRICE_FROM_TICK = None  # "ask" ou "bid"

    def executar(self, symbol, lot, sl, tp, limit, stop, preco):
        """
        Executa o fluxo completo de envio de ordem.

        Retorna um dicionário normalizado com o resultado da operação,
        pronto para ser consumido pela View.

        :raises ValueError: erro de validação de parâmetros
        :return: dict com resultado da ordem
        """

        self._validar_flags(limit, stop)

        if controlar_risco(STATUS_FILE, LOSS_LIMIT):
            msg = "Envio bloqueado por controle de risco"
            log.warning(msg)
            raise RuntimeError(msg)

        tick = obter_tick(symbol)

        order_type, price, pending = self._resolver_tipo_ordem(
            tick=tick,
            limit=limit,
            stop=stop,
            preco=preco,
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

        resultado_mt5 = enviar_ordem_mt5(ordem)

        return self._normalizar_resultado(resultado_mt5, symbol, lot, price)

    # ------------------------------------------------------------------

    @staticmethod
    def _validar_flags(limit, stop):
        if limit and stop:
            raise ValueError("Use apenas --limit OU --stop, nunca ambos.")

    def _resolver_tipo_ordem(self, tick, limit, stop, preco):
        """
        Resolve o tipo da ordem e o preço correto.
        """
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

    # ------------------------------------------------------------------

    @staticmethod
    def _normalizar_resultado(res, symbol, lot, price):
        """
        Normaliza o resultado retornado pelo MT5
        para um formato simples e previsível.
        """
        if res is None:
            raise RuntimeError("Nenhuma resposta recebida do MetaTrader 5")

        sucesso = res.retcode == mt5.TRADE_RETCODE_DONE

        return {
            "sucesso": sucesso,
            "retcode": res.retcode,
            "mensagem": res.comment,
            "ticket": res.order if sucesso else None,
            "symbol": symbol,
            "volume": lot,
            "price": price,
        }
