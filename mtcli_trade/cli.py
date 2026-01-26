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


trade.add_command(buy, name="buy")
trade.add_command(sell, name="sell")
trade.add_command(orders, name="pend")
trade.add_command(positions, name="pos")
trade.add_command(cancel, name="x")
trade.add_command(zera, name="z")
