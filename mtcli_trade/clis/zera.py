"""
Comando para encerrar posições abertas.
"""

import click
from ..controllers.zera_controller import zerar_posicoes


@click.command(
    "zera",
    help="Encerra todas as posições abertas (ou de um ativo específico).",
)
@click.version_option(package_name="mtcli-trade")
@click.option("--symbol", "-s", default=None, help="Símbolo do ativo (opcional)")
def zera(symbol):
    """Zera posições abertas."""
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
