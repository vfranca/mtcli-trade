"""
Comando CLI para cancelamento de ordens pendentes.

Permite:
- Cancelamento unitário por ticket
- Cancelamento em massa por símbolo

Exemplos:

    mt cancel --ticket 123456
    mt cancel --symbol WINM26
"""

import click
from ..controllers.cancel_controller import CancelController


@click.command()
@click.option(
    "--symbol",
    "-s",
    type=str,
    help="Cancela todas as ordens pendentes do ativo informado."
)
@click.option(
    "--ticket",
    "-t",
    type=int,
    help="Cancela ordem pendente específica pelo ticket."
)
def cancel(symbol: str | None, ticket: int | None):
    """
    Cancela ordens pendentes no MT5.

    Regras:
    - Use --ticket para cancelar uma ordem específica.
    - Use --symbol para cancelar todas as ordens de um ativo.
    - Não é permitido usar ambas as opções simultaneamente.
    """

    # ---------------------------
    # Validações
    # ---------------------------

    if not symbol and not ticket:
        raise click.UsageError(
            "Informe --symbol ou --ticket."
        )

    if symbol and ticket:
        raise click.UsageError(
            "Use apenas --symbol OU --ticket."
        )

    controller = CancelController()

    # ---------------------------
    # Cancelamento por símbolo
    # ---------------------------

    if symbol:
        return controller.cancelar_por_symbol(symbol)

    # ---------------------------
    # Cancelamento por ticket
    # ---------------------------

    if ticket:
        return controller.cancelar_por_ticket(ticket)

