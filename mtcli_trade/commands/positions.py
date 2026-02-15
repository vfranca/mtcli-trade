import click
from ..controllers.positions_controller import PositionsController
from ..views.positions_view import exibir_posicoes, exibir_resumo


@click.command()
@click.option(
    "--symbol",
    "-s",
    default=None,
    show_default=True,
    help="Código do símbolo."
)
@click.option(
    "--summary",
    is_flag=True,
    help="Exibe resumo consolidado das posições."
)
def positions(symbol, summary):
    """Lista posições abertas."""

    controller = PositionsController()
    posicoes = controller.obter_posicoes(symbol)

    exibir_posicoes(posicoes, symbol)

    if summary and posicoes:
        resumo = controller.calcular_resumo(posicoes)
        exibir_resumo(resumo)
