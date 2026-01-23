import click
from ..controllers.sell_controller import SellController
from ..conf import SYMBOL, LOT, SL, TP


@click.command("sell")
@click.option("--symbol", "-s", default=SYMBOL)
@click.option("--lot", default=LOT, type=float)
@click.option("-sl", default=SL, type=float)
@click.option("-tp", default=TP, type=float)
@click.option("--limit", is_flag=True)
@click.option("--stop", is_flag=True)
@click.option("--preco", type=float)
def sell(symbol, lot, sl, tp, limit, stop, preco):
    """Envia ordem de VENDA (market | limit | stop)."""
    controller = SellController()
    controller.executar(symbol, lot, sl, tp, limit, stop, preco)
