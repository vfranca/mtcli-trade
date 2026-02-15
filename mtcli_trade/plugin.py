"""
Registro do plugin mtcli-trade no mtcli principal.

Este módulo integra o grupo de comandos do plugin
ao CLI raiz da aplicação.
"""

from .cli import cli as trade


def register(cli):
    """
    Registra o grupo de comandos do plugin no CLI principal.

    Args:
        cli: instância do click.Group principal do mtcli.
    """
    cli.add_command(trade, name="trade")
