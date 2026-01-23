import click
from ..controllers.positions_controller import obter_posicoes
from ..views.positions_view import exibir_posicoes


@click.command("positions")
@click.option("--symbol", "-s", default=None)
def positions(symbol):
    """Lista posições abertas."""
    posicoes = obter_posicoes(symbol)
    exibir_posicoes(posicoes, symbol)
