import click
from ..controllers.buy_controller import BuyController
from ..conf import SYMBOL, LOT, SL, TP


@click.command("buy")
@click.option("--symbol", "-s", default=SYMBOL)
@click.option("--lot", default=LOT, type=float)
@click.option("-sl", default=SL, type=float)
@click.option("-tp", default=TP, type=float)
@click.option("--limit", is_flag=True)
@click.option("--stop", is_flag=True)
@click.option("--preco", type=float)
def buy(symbol, lot, sl, tp, limit, stop, preco):
    """Envia ordem de COMPRA (market | limit | stop)."""
    controller = BuyController()
    controller.executar(symbol, lot, sl, tp, limit, stop, preco)
