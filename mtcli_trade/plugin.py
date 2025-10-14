from mtcli_trade.commands.compra import compra
from mtcli_trade.commands.venda import venda
from mtcli_trade.commands.ordens import ordens
from mtcli_trade.commands.posicoes import posicoes


def register(cli):
    cli.add_command(compra, name="compra")
    cli.add_command(venda, name="venda")
    cli.add_command(ordens, name="ordens")
    cli.add_command(posicoes, name="posicoes")
