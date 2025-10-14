from mtcli_trade.commands.compra_cli import compra_cmd
from mtcli_trade.commands.venda_cli import venda_cmd
from mtcli_trade.commands.ordens import ordens
from mtcli_trade.commands.posicoes import posicoes


def register(cli):
    cli.add_command(compra_cmd, name="compra")
    cli.add_command(venda_cmd, name="venda")
    cli.add_command(ordens, name="ordens")
    cli.add_command(posicoes, name="posicoes")
