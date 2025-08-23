import click
from .compra import compra
from .venda import venda
from .ordens import ordens
from .posicoes import posicoes
from .cancela import cancela
from .zera import zera


@click.group()
@click.version_option(package_name="mtcli-trade")
def trade():
    """CLI para operações no MetaTrader 5."""
    pass


trade.add_command(compra, name="compra")
trade.add_command(venda, name="venda")
trade.add_command(ordens, name="ordens")
trade.add_command(posicoes, name="posicoes")
trade.add_command(cancela, name="cancela")
trade.add_command(zera, name="zera")


if __name__ == "__main__":
    trade()
