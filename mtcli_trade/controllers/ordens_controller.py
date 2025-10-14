from typing import Optional, Sequence
from mtcli_trade.models.ordens_model import (
    buscar_ordens,
    formatar_ordem,
    cancelar_ordens,
)
from mtcli.logger import setup_logger

log = setup_logger()


def obter_ordens_pendentes(symbol=None):
    ordens_raw = buscar_ordens(symbol)

    if not ordens_raw:
        log.info(
            f"Nenhuma ordem pendente para {symbol}."
            if symbol
            else "Nenhuma ordem pendente encontrada"
        )
        return []

    ordens = []
    for o in ordens_raw:
        dados = formatar_ordem(o)
        log.info(
            f"{dados['tipo']} | {dados['symbol']} | volume: {dados['volume']} | preço: {dados['preco']} | ticket: {dados['ticket']}"
        )
        ordens.append(dados)
    return ordens


def cancelar_ordens_pendentes(symbol: Optional[str] = None):
    """Cancelar órdens pendentes (retorna a lista de resultados produzida pelo model)."""
    try:
        resultados = cancelar_ordens(symbol)
    except Exception as e:
        log.error(f"Erro ao cancelar órdens: {e}")
        raise
    return resultados
