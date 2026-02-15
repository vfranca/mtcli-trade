import click
from .commands.trade import trade
from .commands.orders import orders
from .commands.positions import positions
from .commands.cancel import cancel
from .commands.zera import zera


@click.group()
@click.version_option(package_name="mtcli-trade")
def cli():
    pass


cli.add_command(trade, name="trade")
cli.add_command(orders, name="orders")
cli.add_command(positions, name="pos")
cli.add_command(cancel, name="cancel")
cli.add_command(zera, name="zera")
