"""
Comando CLI para listagem de ordens pendentes.

Permite:
- Listar todas as ordens pendentes
- Filtrar por símbolo específico

Exemplos:

    mt orders
    mt orders --symbol WINM26
"""

import click
from ..controllers.orders_controller import OrdersController
from ..views.orders_view import exibir_ordens


@click.command()
@click.option(
    "--symbol",
    "-s",
    default=None,
    show_default=True,
    help="Código do ativo para filtrar ordens pendentes."
)
def orders(symbol: str | None):
    """
    Lista ordens pendentes no MT5.

    Se --symbol for informado, exibe apenas ordens do ativo.
    Caso contrário, lista todas as ordens pendentes.
    """

    controller = OrdersController()
    ordens = controller.obter_ordens_pendentes(symbol)

    exibir_ordens(ordens, symbol)


if __name__ == "__main__":
    orders()
