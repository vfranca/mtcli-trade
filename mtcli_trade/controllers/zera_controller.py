"""
Controller responsável por zerar posições abertas.
"""

from mtcli.logger import setup_logger
from ..services.positions_service import buscar_posicoes_mt5
from ..services.mt5_service import fechar_posicao_mt5

log = setup_logger()


def zerar_posicoes(symbol=None):
    """
    Encerra todas as posições abertas (ou de um símbolo).

    :param symbol: Ativo opcional
    :return: dict com totais
    """
    posicoes = buscar_posicoes_mt5(symbol)

    if not posicoes:
        log.info(
            f"Nenhuma posição para {symbol}"
            if symbol
            else "Nenhuma posição aberta"
        )
        return {"total": 0, "sucesso": 0, "falha": 0}

    sucesso = 0
    falha = 0
    resultados = []

    for p in posicoes:
        try:
            res = fechar_posicao_mt5(p)
            resultados.append(res)
            sucesso += 1
        except Exception as e:
            falha += 1
            log.error(f"Falha ao fechar posição {p.ticket}: {e}")

    return {
        "total": len(posicoes),
        "sucesso": sucesso,
        "falha": falha,
        "resultados": resultados,
    }
