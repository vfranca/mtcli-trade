import click
from ..controllers.positions_controller import PositionsController
from ..views.positions_view import exibir_posicoes


@click.command()
@click.option(
    "--symbol",
    "-s",
    default=None,
    show_default=True,
    help="Código do símbolo."
)
def positions(symbol):
    """Lista posições abertas."""

    controller = PositionsController()
    posicoes = controller.obter_posicoes(symbol)

    exibir_posicoes(posicoes, symbol)
