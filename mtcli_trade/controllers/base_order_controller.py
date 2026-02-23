"""
Controller base para envio de ordens.
"""

import MetaTrader5 as mt5
from ..services.mt5_service import MT5Service
from ..strategies.strategy_factory import StrategyFactory
from ..conf import DIGITOS


class BaseOrderController:

    ORDER_TYPE_MARKET = {
        "buy": mt5.ORDER_TYPE_BUY,
        "sell": mt5.ORDER_TYPE_SELL,
    }

    ORDER_TYPE_LIMIT = {
        "buy": mt5.ORDER_TYPE_BUY_LIMIT,
        "sell": mt5.ORDER_TYPE_SELL_LIMIT,
    }

    ORDER_TYPE_STOP = {
        "buy": mt5.ORDER_TYPE_BUY_STOP,
        "sell": mt5.ORDER_TYPE_SELL_STOP,
    }

    PRICE_FROM_TICK = {
        "buy": "ask",
        "sell": "bid",
    }

    def __init__(self, side: str):
        self.side = side.lower()
        self.mt5 = MT5Service()

    # =====================================================
    # EXECUÇÃO PRINCIPAL
    # =====================================================

    def executar(
        self,
        symbol: str,
        lot: float,
        sl: float | None,
        tp: float | None,
        limit: bool,
        stop: bool,
        preco: float | None,
    ):
        tick = self.mt5.obter_tick(symbol)

        strategy = StrategyFactory.create(limit, stop)

        order_type = self._definir_tipo(strategy)
        price = strategy.definir_preco(self, tick, preco)

        point = mt5.symbol_info(symbol).point

        sl_price = self._calcular_sl(price, sl, point)
        tp_price = self._calcular_tp(price, tp, point)

        request = self._montar_request(
            symbol, lot, order_type, price, sl_price, tp_price
        )

        return self.mt5.enviar_request(request)

    # =====================================================
    # AUXILIARES
    # =====================================================

    def _definir_tipo(self, strategy):
        if strategy.__class__.__name__ == "MarketStrategy":
            return self.ORDER_TYPE_MARKET[self.side]

        if strategy.__class__.__name__ == "LimitStrategy":
            return self.ORDER_TYPE_LIMIT[self.side]

        return self.ORDER_TYPE_STOP[self.side]

    def _calcular_sl(self, price, sl, point):
        if sl is None:
            return None

        if self.side == "buy":
            valor = price - (sl * point)
        else:
            valor = price + (sl * point)

        return round(valor, DIGITOS)

    def _calcular_tp(self, price, tp, point):
        if tp is None:
            return None

        if self.side == "buy":
            valor = price + (tp * point)
        else:
            valor = price - (tp * point)

        return round(valor, DIGITOS)

    def _montar_request(self, symbol, lot, order_type, price, sl, tp):

        request = {
            "action": mt5.TRADE_ACTION_DEAL
            if order_type in (
                mt5.ORDER_TYPE_BUY,
                mt5.ORDER_TYPE_SELL,
            )
            else mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": lot,
            "type": order_type,
            "price": price,
            "deviation": 10,
            "magic": 123456,
            "comment": "mtcli-trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        if sl is not None:
            request["sl"] = sl

        if tp is not None:
            request["tp"] = tp

        return request
