from .cli import trade
from .clis.buy import buy
from .clis.sell import sell
from .clis.orders import orders
from .clis.cancel import cancel
from .clis.positions import positions
from .clis.zera import zera


def register(cli):
    cli.add_command(trade, name="trade")
    cli.add_command(buy, name="buy")
    cli.add_command(sell, name="sell")
    cli.add_command(orders, name="orders")
    cli.add_command(cancel, name="cancel")
    cli.add_command(positions, name="pos")
    cli.add_command(zera, name="zera")
