"""
CLI principal do plugin mtcli-trade.

Este módulo define o grupo de comandos responsáveis
pela execução e gerenciamento operacional no MetaTrader 5.

Comandos disponíveis:

- send     → Envio de ordens
- orders   → Listagem de ordens pendentes
- cancel   → Cancelamento de ordens
- pos      → Listagem de posições abertas
- close    → Fechamento de posições

Este grupo é registrado no mtcli principal através do
mecanismo de plugin.
"""

import click
from .commands.trade import trade
from .commands.orders import orders
from .commands.cancel import cancel
from .commands.positions import positions
from .commands.close import close
from .commands.monitor import monitor


@click.group()
@click.version_option(package_name="mtcli-trade")
def cli():
    """
    Comandos operacionais de trading e gestão de ordens/posições.
    """
    # Grupo raiz do plugin — não executa ação direta
    return None


cli.add_command(trade, name="send")
cli.add_command(orders, name="orders")
cli.add_command(cancel, name="cancel")
cli.add_command(positions, name="pos")
cli.add_command(close, name="close")
cli.add_command(monitor, name="monitor")
