"""
Controller genérico com Strategy Pattern.
Retorna resultado normalizado (dict).
"""

import MetaTrader5 as mt5
from ..decorators.mt5_connection import with_mt5
from ..strategies.strategy_factory import StrategyFactory
from ..services.mt5_service import MT5Service
from ..events.event_bus import event_bus
from ..events.events import POSITION_OPENED


class OrderController:
    """
    Controller configurável via Strategy Pattern.
    """

    def __init__(
        self,
        order_type_market,
        order_type_limit,
        order_type_stop,
        price_from_tick,
    ):
        self.ORDER_TYPE_MARKET = order_type_market
        self.ORDER_TYPE_LIMIT = order_type_limit
        self.ORDER_TYPE_STOP = order_type_stop
        self.PRICE_FROM_TICK = price_from_tick

        self.mt5_service = MT5Service()

    # -----------------------------------------------------

    @with_mt5
    def executar(
        self,
        symbol,
        lot,
        sl,
        tp,
        limit=False,
        stop=False,
        preco=None,
    ):
        """
        Executa ordem.
        SL e TP são informados em pontos.
        Retorna dict padronizado.
        """

        strategy = StrategyFactory.create(limit, stop)

        tick = self.mt5_service.obter_tick(symbol)
        if not tick:
            raise RuntimeError("Não foi possível obter tick.")

        order_type = strategy.definir_tipo_ordem(self)
        price = strategy.definir_preco(self, tick, preco)

        is_market = not (limit or stop)

        sl_price, tp_price = self._calcular_sl_tp(
            symbol, price, sl, tp, order_type
        )

        request = {
            "action": (
                mt5.TRADE_ACTION_DEAL
                if is_market
                else mt5.TRADE_ACTION_PENDING
            ),
            "symbol": symbol,
            "volume": lot,
            "type": order_type,
            "price": price,
            "sl": sl_price,
            "tp": tp_price,
            "deviation": 20,
            "magic": 123456,
            "comment": "mtcli-trade order",
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        resultado = self.mt5_service.enviar_request(request)

        sucesso = resultado.retcode in (
            mt5.TRADE_RETCODE_DONE,
            mt5.TRADE_RETCODE_PLACED,
        )

        if is_market and sucesso:
            event_bus.publish(
                POSITION_OPENED,
                symbol=symbol,
                volume=lot,
            )

        return {
            "sucesso": sucesso,
            "retcode": resultado.retcode,
            "mensagem": resultado.comment,
            "ticket": resultado.order if sucesso else None,
            "symbol": symbol,
            "volume": lot,
            "price": price,
        }

    # -----------------------------------------------------

    def _calcular_sl_tp(
        self,
        symbol,
        price,
        sl_pontos,
        tp_pontos,
        order_type,
    ):
        info = mt5.symbol_info(symbol)
        if not info:
            raise RuntimeError(f"Não foi possível obter info de {symbol}")

        point = info.point

        sl = None
        tp = None

        if order_type == mt5.ORDER_TYPE_BUY:
            if sl_pontos:
                sl = price - (sl_pontos * point)
            if tp_pontos:
                tp = price + (tp_pontos * point)

        elif order_type == mt5.ORDER_TYPE_SELL:
            if sl_pontos:
                sl = price + (sl_pontos * point)
            if tp_pontos:
                tp = price - (tp_pontos * point)

        return sl, tp
