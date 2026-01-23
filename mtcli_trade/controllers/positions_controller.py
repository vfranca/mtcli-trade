"""
Controller de posições abertas.
"""

from mtcli.logger import setup_logger
from ..services.positions_service import buscar_posicoes_mt5
from ..models.positions_model import normalizar_posicao

log = setup_logger()


def obter_posicoes(symbol=None):
    posicoes_raw = buscar_posicoes_mt5(symbol)

    if not posicoes_raw:
        log.info(
            f"Nenhuma posição para {symbol}"
            if symbol
            else "Nenhuma posição aberta"
        )
        return []

    return [normalizar_posicao(p) for p in posicoes_raw]
