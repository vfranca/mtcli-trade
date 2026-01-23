import click
from .clis.buy import buy
from .clis.sell import sell
from .clis.orders import orders
from .clis.positions import positions
from .clis.cancel import cancel
from .clis.zera import zera


@click.group()
@click.version_option(package_name="mtcli-trade")
def trade():
    pass


trade.add_command(buy)
trade.add_command(sell)
trade.add_command(orders)
trade.add_command(positions)
trade.add_command(cancel)
trade.add_command(zera)
