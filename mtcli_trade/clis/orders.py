import click
from ..controllers.orders_controller import obter_ordens_pendentes
from ..views.orders_view import exibir_ordens


@click.command()
@click.option("--symbol", "-s", default=None, show_default=True, help="Codigo do ativo.")
def orders(symbol):
    """Lista todas as ordens pendentes (ou de um símbolo)"""
    ordens = obter_ordens_pendentes(symbol)
    exibir_ordens(ordens, symbol)


if __name__ == "__main__":
    orders()
