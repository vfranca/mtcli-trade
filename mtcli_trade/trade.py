import click
from mtcli_trade.commands.compra import compra
from mtcli_trade.commands.venda import venda
from mtcli_trade.commands.ordens import ordens
from mtcli_trade.commands.posicoes import posicoes


@click.group()
@click.version_option(package_name="mtcli-trade")
def trade():
    """Comandos para execucao e gerenciamento de trades."""
    pass


trade.add_command(compra, name="compra")
trade.add_command(venda, name="venda")
trade.add_command(ordens, name="ordens")
trade.add_command(posicoes, name="posicoes")
