from .cli import trade


def register(cli):
    cli.add_command(trade, name="trade")
