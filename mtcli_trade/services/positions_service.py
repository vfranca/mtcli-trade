"""
Serviços de acesso a posições abertas via MetaTrader 5 (MT5).

Este módulo é responsável exclusivamente por:
- Buscar posições abertas
- Não contém lógica de negócio
- Não formata dados
- Não interage com CLI ou Click

Controllers e models não devem acessar o MT5 diretamente.
"""

import MetaTrader5 as mt5
from mtcli.conecta import conectar, shutdown


def buscar_posicoes_mt5(symbol=None):
    """
    Retorna posições abertas no MT5.

    :param symbol: Ativo opcional (ex: WIN, WDO)
    :return: tuple de posições MT5 ou None
    """
    conectar()
    try:
        return mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()
    finally:
        shutdown()
