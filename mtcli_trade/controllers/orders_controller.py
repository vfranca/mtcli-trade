"""
Controller responsável por obter ordens pendentes.
"""

from mtcli.logger import setup_logger
from ..services.orders_service import buscar_ordens_mt5
from ..models.orders_model import normalizar_ordem

log = setup_logger()


def obter_ordens_pendentes(symbol=None):
    """
    Retorna uma lista normalizada de ordens pendentes.
    """
    ordens_raw = buscar_ordens_mt5(symbol)

    if not ordens_raw:
        log.info(
            f"Nenhuma ordem pendente para {symbol}"
            if symbol
            else "Nenhuma ordem pendente encontrada"
        )
        return []

    ordens = [normalizar_ordem(o) for o in ordens_raw]

    for o in ordens:
        log.info(
            f"{o['tipo']} | {o['symbol']} | vol {o['volume']} | preço {o['preco']} | ticket {o['ticket']}"
        )

    return ordens
