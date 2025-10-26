import MetaTrader5 as mt5
from mtcli.mt5_context import mt5_conexao
from mtcli.logger import setup_logger

log = setup_logger()


def inicializar(symbol):
    with mt5_conexao():
        if not mt5.symbol_select(symbol, True):
            log.error(f"Erro ao selecionar símbolo {symbol}")
            return None
        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            log.error(f"Erro ao obter preco de {symbol}")
            return None

    return tick


def criar_ordem(symbol, lot, sl, tp, price, order_type, limit):
    info = mt5.symbol_info(symbol)
    point = info.point if info else 0.01  # fallback

    sl_price = (
        price - sl * point
        if order_type in (mt5.ORDER_TYPE_BUY, mt5.ORDER_TYPE_BUY_LIMIT)
        else price + sl * point
    )
    tp_price = (
        price + tp * point
        if order_type in (mt5.ORDER_TYPE_BUY, mt5.ORDER_TYPE_BUY_LIMIT)
        else price - tp * point
    )

    return {
        "action": mt5.TRADE_ACTION_PENDING if limit else mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl_price,
        "tp": tp_price,
        "deviation": 10,
        "magic": 1000,
        "comment": "Ordem mtcli",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }


def enviar_ordem(ordem, limit):
    log.info(f"Enviando ordem: {ordem}")
    resultado = mt5.order_send(ordem)
    log.debug(f"Resultado do envio da órdem models.ordem.py: {ordem}")
    if resultado.retcode in (mt5.TRADE_RETCODE_DONE, mt5.TRADE_RETCODE_PLACED):
        msg = f"Ordem {'limitada' if limit else 'a mercado'} enviada com sucesso ticket {resultado.order}"
        click.echo(msg)
        log.info(msg)
    else:
        msg = f"Falha ao enviar órdem {resultado.retcode} - {resultado.comment}"
        click.echo(msg)
        log.error(msg)
    return resultado
