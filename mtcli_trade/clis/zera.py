"""
Comando para encerrar posições abertas.
"""

import click
from ..controllers.zera_controller import zerar_posicoes


@click.command()
@click.option("--symbol", "-s", default=None, show_default=True, help="Codigo do simbolo.")
def zera(symbol):
    """Zera todas as posições abertas ou de um simbolo."""
    resultado = zerar_posicoes(symbol)

    if resultado["total"] == 0:
        click.echo(
            f"Não existem posições abertas para {symbol}"
            if symbol
            else "Não existem posições abertas."
        )
        return

    click.echo(
        f"Encerradas {resultado['sucesso']} de {resultado['total']} posições."
    )

    if resultado["falha"]:
        click.echo(f"Falhas: {resultado['falha']}")
