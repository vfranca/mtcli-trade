import MetaTrader5 as mt5
from mtcli.mt5_context import mt5_conexao
from mtcli.logger import setup_logger
from mtcli_trade.conf import LOSS_LIMIT, STATUS_FILE
from mtcli_trade.models.risco_model import controlar_risco

log = setup_logger()


def verificar_risco():
    """Verifica se o risco diário permite novas ordens."""
    if controlar_risco(STATUS_FILE, LOSS_LIMIT):
        return {
            "status": "bloqueado",
            "codigo": -1,
            "mensagem": "Ordem bloqueada: limite de prejuízo diário atingido",
            "preco": 0.00,
        }
    return None


def obter_tick(symbol):
    """Obtém o último tick do símbolo selecionado."""
    with mt5_conexao():
        if not mt5.symbol_select(symbol, True):
            log.error(f"Erro ao selecionar símbolo {symbol}")
            return None
        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            log.error(f"Erro ao obter preço de {symbol}")
            return None
    return tick


def criar_ordem_compra(symbol, lot, sl, tp, price, order_type, limit):
    """Cria uma estrutura de ordem para compra."""
    info = mt5.symbol_info(symbol)
    point = info.point if info else 0.01
    sl_price = price - sl * point
    tp_price = price + tp * point

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


def enviar_ordem_compra(ordem):
    """Envia a ordem ao MetaTrader 5 e retorna o resultado formatado."""
    resultado = mt5.order_send(ordem)
    status = "sucesso" if resultado.retcode in (mt5.TRADE_RETCODE_DONE, mt5.TRADE_RETCODE_PLACED) else "falha"
    return {
        "status": status,
        "codigo": resultado.retcode,
        "mensagem": resultado.comment,
        "preco": resultado.price,
    }


def enviar_compra(symbol, lot, sl, tp, limit, preco):
    """Executa uma ordem de compra completa (a mercado ou pendente)."""
    tick = obter_tick(symbol)
    if not tick:
        return {
            "status": "falha",
            "codigo": -1,
            "mensagem": "Não foi possível obter o preço atual",
            "preco": 0.00,
        }

    if limit:
        if preco is None:
            return {
                "status": "falha",
                "codigo": -1,
                "mensagem": "Para ordens pendentes, defina o --preco",
                "preco": 0.00,
            }
        price = preco
        order_type = mt5.ORDER_TYPE_BUY_LIMIT
    else:
        price = tick.ask
        order_type = mt5.ORDER_TYPE_BUY

    ordem = criar_ordem_compra(symbol, lot, sl, tp, price, order_type, limit)
    return enviar_ordem_compra(ordem)
