"""Comando principal do plugin."""

import click

from .buy import buy
from .cancel import cancel
from .orders import orders
from .pos import pos
from .sell import sell
from .zera import zera


@click.group("trade")
@click.version_option(package_name="mtcli-trade")
def cli():
    """Gerencia operações no MetaTrader 5."""
    pass


cli.add_command(buy, name="buy")
cli.add_command(sell, name="sell")
cli.add_command(orders, name="orders")
cli.add_command(pos, name="pos")
cli.add_command(cancel, name="cancel")
cli.add_command(zera, name="zera")


if __name__ == "__main__":
    cli()
