"""
Serviço de acesso a posições abertas.

Camada fina sobre MT5Service.
"""

from .mt5_service import MT5Service

mt5_service = MT5Service()


def buscar_posicoes_mt5(symbol: str | None = None):
    """
    Retorna posições abertas.

    :param symbol: ativo opcional
    :return: tuple de posições
    """
    return mt5_service.obter_posicoes(symbol)
