"""
Controller responsável pelo cancelamento de ordens pendentes.
"""

from mtcli.logger import setup_logger
from ..services.orders_service import buscar_ordens_mt5
from ..services.mt5_service import cancelar_ordem_mt5

log = setup_logger()


def cancelar_ordens(symbol=None):
    """
    Cancela todas as ordens pendentes ou apenas de um símbolo.

    :param symbol: Ativo (opcional)
    :return: dict com totais
    """
    ordens = buscar_ordens_mt5(symbol)

    if not ordens:
        log.info(
            f"Nenhuma ordem pendente para {symbol}"
            if symbol
            else "Nenhuma ordem pendente encontrada"
        )
        return {"total": 0, "sucesso": 0, "falha": 0}

    sucesso = 0
    falha = 0

    for o in ordens:
        try:
            cancelar_ordem_mt5(o)
            sucesso += 1
            log.info(f"Ordem cancelada: {o.ticket} ({o.symbol})")
        except Exception as e:
            falha += 1
            log.error(f"Falha ao cancelar {o.ticket}: {e}")

    return {
        "total": len(ordens),
        "sucesso": sucesso,
        "falha": falha,
    }
