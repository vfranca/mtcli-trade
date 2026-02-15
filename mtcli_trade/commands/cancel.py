import click
from ..controllers.cancel_controller import CancelController


@click.command()
@click.option(
    "--ticket",
    "-t",
    type=int,
    help="Ticket da ordem pendente."
)
@click.option(
    "--symbol",
    "-s",
    type=str,
    help="Cancela todas as ordens pendentes do ativo."
)
def cancel(ticket, symbol):
    """
    Cancela ordem por ticket ou em massa por símbolo.
    """

    if not ticket and not symbol:
        raise click.UsageError(
            "Informe --ticket ou --symbol."
        )

    if ticket and symbol:
        raise click.UsageError(
            "Use apenas --ticket OU --symbol."
        )

    controller = CancelController()

    if ticket:
        controller.cancelar_por_ticket(ticket)

    if symbol:
        controller.cancelar_por_symbol(symbol)


if __name__ == "__main__":
    cancel()
