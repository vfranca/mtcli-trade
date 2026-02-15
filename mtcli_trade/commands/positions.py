import click
from ..controllers.positions_controller import obter_posicoes
from ..views.positions_view import exibir_posicoes


@click.command()
@click.option("--symbol", "-s", default=None, show_default=True, help="Codigo do simbolo.")
def positions(symbol):
    """Lista posições abertas."""
    posicoes = obter_posicoes(symbol)
    exibir_posicoes(posicoes, symbol)
