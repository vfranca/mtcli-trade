import MetaTrader5 as mt5
from mtcli_trade.models.risco_model import controlar_risco
from mtcli_trade.models.ordem_model import inicializar, criar_ordem, enviar_ordem
from mtcli_trade.conf import STATUS_FILE, LOSS_LIMIT
from mtcli.logger import setup_logger

log = setup_logger()


def verificar_risco() -> bool:
    """Retorna True se o risco bloquear a operação."""
    return controlar_risco(STATUS_FILE, LOSS_LIMIT)


def preparar_ordem_compra(
    symbol: str, lot: float, sl: float, tp: float, limit: bool, preco: float = None
):
    """Prepara a ordem de compra a mercado ou pendente."""
    tick = inicializar(symbol)
    if not tick:
        log.error("Falha ao inicializar tick para símbolo %s", symbol)
        return None, None

    if limit:
        if preco is None:
            raise ValueError("Preço obrigatório para ordens pendentes (limit).")
        price = preco
        order_type = mt5.ORDER_TYPE_BUY_LIMIT
    else:
        price = tick.ask
        order_type = mt5.ORDER_TYPE_BUY

    ordem = criar_ordem(symbol, lot, sl, tp, price, order_type, limit)
    return ordem, limit


def enviar_ordem_compra(ordem, limit: bool):
    """Envia a ordem de compra via MetaTrader5."""
    if not ordem:
        log.error("Ordem inválida, cancelando envio.")
        return None
    return enviar_ordem(ordem, limit)
