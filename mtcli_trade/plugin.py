from .cli import cli as manager
from .commands.trade import trade
from .commands.orders import orders
from .commands.cancel import cancel
from .commands.positions import positions
from .commands.zera import zera


def register(cli):
    cli.add_command(manager, name="manager")
    cli.add_command(trade, name="trade")
    cli.add_command(orders, name="orders")
    cli.add_command(cancel, name="cancel")
    cli.add_command(positions, name="pos")
    cli.add_command(zera, name="zera")
