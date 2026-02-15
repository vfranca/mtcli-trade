"""
Comando CLI para listagem de posições abertas.

Permite:
- Listar todas as posições abertas
- Filtrar por símbolo específico
- Exibir resumo consolidado (volume, lucro, swap)

Exemplos:

    mt positions
    mt positions --symbol WINM26
    mt positions --symbol WINM26 --summary
"""

import click
from ..controllers.positions_controller import PositionsController
from ..views.positions_view import (
    exibir_posicoes,
    exibir_resumo,
)


@click.command()
@click.option(
    "--symbol",
    "-s",
    default=None,
    show_default=True,
    help="Código do símbolo para filtrar posições abertas."
)
@click.option(
    "--summary",
    is_flag=True,
    help="Exibe resumo consolidado das posições listadas."
)
def positions(symbol: str | None, summary: bool):
    """
    Lista posições abertas no MT5.

    Se --symbol for informado, exibe apenas posições do ativo.
    Caso contrário, lista todas as posições abertas.

    Use --summary para exibir resumo consolidado.
    """

    controller = PositionsController()
    posicoes = controller.obter_posicoes(symbol)

    exibir_posicoes(posicoes, symbol)

    if summary and posicoes:
        resumo = controller.calcular_resumo(posicoes)
        exibir_resumo(resumo)
