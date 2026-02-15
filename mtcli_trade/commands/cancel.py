import click
from ..controllers.cancel_controller import CancelController
from ..views.cancel_view import exibir_resultado_cancelamento


@click.command()
@click.option(
    "--ticket",
    "-t",
    required=True,
    type=int,
    help="Ticket da ordem pendente."
)
def cancel(ticket):
    """
    Cancela uma ordem pendente pelo ticket.
    """

    controller = CancelController()

    resultado = controller.cancelar(ticket)

    exibir_resultado_cancelamento(resultado, ticket)


if __name__ == "__main__":
    cancel()
