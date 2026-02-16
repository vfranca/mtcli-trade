"""
Comando CLI para monitoramento contínuo de posições.
"""

import click
from ..monitor.positions_monitor import PositionsMonitor


@click.command()
@click.option(
    "--symbol",
    "-s",
    default=None,
    help="Monitora apenas posições do símbolo informado."
)
@click.option(
    "--interval",
    "-i",
    default=1.0,
    show_default=True,
    help="Intervalo de atualização em segundos."
)
def monitor(symbol, interval):
    """
    Inicia monitor contínuo de posições abertas.
    """

    monitor = PositionsMonitor(symbol, interval)
    monitor.iniciar()
