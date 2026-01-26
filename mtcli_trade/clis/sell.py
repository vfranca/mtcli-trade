import click
from ..controllers.sell_controller import SellController
from ..conf import SYMBOL, LOT, SL, TP


@click.command()
@click.option("--symbol", "-s", default=SYMBOL, show_default=True, help="Codigo do symbol.")
@click.option("--lot", "-l", default=LOT, type=float, show_default=True, help="Quantidade de lotes.")
@click.option("-sl", default=SL, type=float, show_default=True, help="Stop loss em pontos.")
@click.option("-tp", default=TP, type=float, show_default=True, help="Take profit em pontos.")
@click.option("--limit", "-lm", is_flag=True, help="Ordem limitada.")
@click.option("--stop", "-st", is_flag=True, help="Ordem stop.")
@click.option("--preco", "-p", type=float, help="Preco de entrada para ordem pendente.")
def sell(symbol, lot, sl, tp, limit, stop, preco):
    """Envia ordem de VENDA (market | limit | stop)."""
    controller = SellController()
    controller.executar(symbol, lot, sl, tp, limit, stop, preco)
