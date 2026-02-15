"""
Serviço de acesso às ordens pendentes.

Não acessa MetaTrader diretamente.
Utiliza MT5Service como infraestrutura.
"""

from .mt5_service import MT5Service

mt5_service = MT5Service()


def buscar_ordens_mt5(symbol: str | None = None):
    """
    Retorna ordens pendentes.

    :param symbol: símbolo opcional
    :return: tuple de ordens
    """
    return mt5_service.obter_ordens(symbol)
