"""
Controller genérico com Strategy Pattern.
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
        Executa ordem utilizando Strategy Pattern.
        """

        strategy = StrategyFactory.create(limit, stop)

        tick = self.mt5_service.obter_tick(symbol)

        order_type = strategy.definir_tipo_ordem(self)
        price = strategy.definir_preco(self, tick, preco)

        is_market = not (limit or stop)

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
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 123456,
            "comment": "mtcli-trade order",
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        resultado = self.mt5_service.enviar_request(request)

        # Evento apenas para execução imediata (market)
        if (
            is_market
            and resultado
            and resultado.retcode == mt5.TRADE_RETCODE_DONE
        ):
            event_bus.publish(
                POSITION_OPENED,
                symbol=symbol,
                volume=lot,
            )

        return resultado
