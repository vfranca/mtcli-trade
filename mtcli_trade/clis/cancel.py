"""
Cancela ordens pendentes.
"""

import click
from ..controllers.cancel_controller import cancelar_ordens


@click.command()
@click.option("--symbol", "-s", default=None, show_default=True, help="Símbolo do ativo (opcional)")
def cancel(symbol):
    """Cancela ordens pendentes (todas ou por simbolo)."""
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
