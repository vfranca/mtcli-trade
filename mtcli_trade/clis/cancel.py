"""
Cancela ordens pendentes.
"""

import click
from ..controllers.cancel_controller import cancelar_ordens


@click.command(
    "cancel",
    help="Cancela ordens pendentes (todas ou por símbolo).",
)
@click.version_option(package_name="mtcli-trade")
@click.option("--symbol", "-s", default=None, help="Símbolo do ativo (opcional)")
def cancel(symbol):
    """Cancela ordens pendentes."""
    resultado = cancelar_ordens(symbol)

    if resultado["total"] == 0:
        click.echo(
            f"Nenhuma ordem pendente para {symbol}"
            if symbol
            else "Nenhuma ordem pendente encontrada."
        )
        return

    click.echo(
        f"Canceladas {resultado['sucesso']} de {resultado['total']} ordens."
    )

    if resultado["falha"]:
        click.echo(f"Falhas: {resultado['falha']}")
