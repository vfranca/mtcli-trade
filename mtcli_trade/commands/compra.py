import click
from mtcli_trade.controllers.compra_controller import processar_compra
from mtcli_trade.views.compra_view import exibir_compra
from mtcli_trade.conf import SYMBOL, LOT, SL, TP


@click.command(help="Envia ordem de compra a mercado ou pendente, com SL e TP opcionais.")
@click.version_option(package_name="mtcli-trade")
@click.option("--symbol", "-s", default=SYMBOL, help="Símbolo do ativo (ex: WINV25).")
@click.option("--lot", type=float, default=LOT, help="Quantidade de contratos (default 1.0).")
@click.option("-sl", type=float, default=SL, help="Stop loss em pontos (default 150).")
@click.option("-tp", type=float, default=TP, help="Take profit em pontos (default 300).")
@click.option("--limit", "-l", is_flag=True, help="Envia ordem pendente (buy limit).")
@click.option("--preco", "-pr", type=float, default=None, help="Preço da ordem pendente (buy limit).")
def compra(symbol, lot, sl, tp, limit, preco):
    """Compra a mercado ou pendente com SL e TP."""
    resultado = processar_compra(symbol=symbol, lot=lot, sl=sl, tp=tp, limit=limit, preco=preco)
    exibir_compra(resultado)
