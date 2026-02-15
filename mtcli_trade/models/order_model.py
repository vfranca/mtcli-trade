"""
Modelo responsável por criar e validar ordens MT5.

Funções:
- Converter SL/TP de pontos para preço
- Validar distância mínima de stops
- Validar lado correto (BUY/SELL)
- Gerar payload seguro para mt5.order_send
"""

import MetaTrader5 as mt5


def criar_ordem(symbol, lot, sl, tp, price, order_type, pending):

    if sl is not None and sl < 0:
        raise ValueError("Stop loss não pode ser negativo")

    if tp is not None and tp < 0:
        raise ValueError("Take profit não pode ser negativo")

    info = mt5.symbol_info(symbol)
    if info is None:
        raise ValueError(f"Ativo inválido ou não encontrado: {symbol}")

    point = info.point
    stop_level = info.trade_stops_level
    min_dist = stop_level * point

    is_buy = order_type in (
        mt5.ORDER_TYPE_BUY,
        mt5.ORDER_TYPE_BUY_LIMIT,
        mt5.ORDER_TYPE_BUY_STOP,
    )

    sl_price = None
    tp_price = None

    if sl and sl > 0:
        sl_price = price - sl * point if is_buy else price + sl * point

    if tp and tp > 0:
        tp_price = price + tp * point if is_buy else price - tp * point

    _validar_stops(
        price, sl_price, tp_price, min_dist, is_buy, symbol, stop_level
    )

    payload = {
        "action": mt5.TRADE_ACTION_PENDING if pending else mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "deviation": 10,
        "magic": 1000,
        "comment": "mtcli-trade",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    if sl_price:
        payload["sl"] = sl_price

    if tp_price:
        payload["tp"] = tp_price

    return payload


def _validar_stops(price, sl_price, tp_price, min_dist, is_buy, symbol, stop_level):

    if sl_price is not None:
        dist_sl = abs(price - sl_price)

        if dist_sl < min_dist:
            raise ValueError(
                f"Stop loss inválido para {symbol}: mínimo exigido {stop_level} pontos"
            )

        if is_buy and sl_price >= price:
            raise ValueError("Em BUY o SL deve ser menor que o preço")

        if not is_buy and sl_price <= price:
            raise ValueError("Em SELL o SL deve ser maior que o preço")

    if tp_price is not None:
        dist_tp = abs(price - tp_price)

        if dist_tp < min_dist:
            raise ValueError(
                f"Take profit inválido para {symbol}: mínimo exigido {stop_level} pontos"
            )

        if is_buy and tp_price <= price:
            raise ValueError("Em BUY o TP deve ser maior que o preço")

        if not is_buy and tp_price >= price:
            raise ValueError("Em SELL o TP deve ser menor que o preço")
