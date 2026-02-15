import click
from ..controllers.close_controller import CloseController
from ..views.close_view import exibir_resultado_fechamento


@click.command()
@click.option(
    "--symbol",
    "-s",
    required=True,
    help="Fecha todas as posições abertas do símbolo."
)
def close(symbol):
    """
    Fecha posições abertas por símbolo.
    """

    controller = CloseController()

    resultados = controller.fechar_por_symbol(symbol)

    exibir_resultado_fechamento(resultados, symbol)


if __name__ == "__main__":
    close()
