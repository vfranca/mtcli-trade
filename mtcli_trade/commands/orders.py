import click
from ..controllers.orders_controller import OrdersController
from ..views.orders_view import exibir_ordens


@click.command()
@click.option(
    "--symbol", "-s",
    default=None,
    show_default=True,
    help="Código do ativo."
)
def orders(symbol):
    """Lista todas as ordens pendentes (ou de um símbolo)."""

    controller = OrdersController()
    ordens = controller.obter_ordens_pendentes(symbol)

    exibir_ordens(ordens, symbol)


if __name__ == "__main__":
    orders()
