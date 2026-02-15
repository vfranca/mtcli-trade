"""
Comando CLI para fechamento de posições abertas.

Permite:
- Fechar todas as posições abertas de um símbolo específico

Exemplos:

    mt close --symbol WINM26
"""

import click
from ..controllers.close_controller import CloseController
from ..views.close_view import exibir_resultado_fechamento


@click.command()
@click.option(
    "--symbol",
    "-s",
    required=True,
    help="Código do símbolo cujas posições serão fechadas."
)
def close(symbol: str):
    """
    Fecha todas as posições abertas do símbolo informado.

    O fechamento é realizado posição por posição.
    """

    controller = CloseController()

    resultados = controller.fechar_por_symbol(symbol)

    exibir_resultado_fechamento(resultados, symbol)


if __name__ == "__main__":
    close()
