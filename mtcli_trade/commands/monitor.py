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
@click.option(
    "--targets",
    "-t",
    default="1",
    show_default=True,
    help="Alvos em R separados por vírgula (ex: 1,2,3)."
)
@click.option(
    "--partials",
    "-p",
    default="0.5",
    show_default=True,
    help="Percentuais de parcial correspondentes (ex: 0.5,0.5)."
)
@click.option(
    "--daily-stop",
    type=float,
    default=None,
    help="Stop diário financeiro (valor negativo máximo permitido)."
)
def monitor(symbol, interval, targets, partials, daily_stop):
    """
    Inicia monitor contínuo com multi-alvos e stop diário.
    """

    targets_list = [float(x.strip()) for x in targets.split(",")]
    partials_list = [float(x.strip()) for x in partials.split(",")]

    if len(targets_list) != len(partials_list):
        raise click.UsageError(
            "Targets e partials devem ter o mesmo tamanho."
        )

    monitor = PositionsMonitor(
        symbol=symbol,
        interval=interval,
        targets=targets_list,
        partials=partials_list,
        daily_stop=daily_stop,
    )

    monitor.iniciar()
