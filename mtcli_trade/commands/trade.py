"""
Comando único para envio de ordens (BUY ou SELL).
"""

import click
from ..controllers.order_factory import OrderFactory
from ..views.order_view import exibir_resultado_ordem
from ..conf import SYMBOL, LOT, SL, TP


@click.command()
@click.option(
    "--side", "-sd",
    type=click.Choice(["buy", "sell"], case_sensitive=False),
    required=True,
    help="Lado da operação: buy ou sell."
)
@click.option(
    "--symbol", "-s",
    default=SYMBOL,
    show_default=True,
    help="Código do ativo."
)
@click.option(
    "--lot", "-l",
    default=LOT,
    type=float,
    show_default=True,
    help="Quantidade de lotes."
)
@click.option(
    "-sl",
    default=SL,
    type=float,
    show_default=True,
    help="Stop loss em pontos."
)
@click.option(
    "-tp",
    default=TP,
    type=float,
    show_default=True,
    help="Take profit em pontos."
)
@click.option(
    "--limit", "-lm",
    is_flag=True,
    help="Envia ordem limitada."
)
@click.option(
    "--stop", "-st",
    is_flag=True,
    help="Envia ordem stop."
)
@click.option(
    "--price", "-p",
    type=float,
    help="Preço de entrada para ordem pendente."
)
def trade(side, symbol, lot, sl, tp, limit, stop, price):
    """
    Envia ordem de compra ou venda (market, limit ou stop).
    """

    controller = OrderFactory.create(side)

    try:
        resultado = controller.executar(
            symbol=symbol,
            lot=lot,
            sl=sl,
            tp=tp,
            limit=limit,
            stop=stop,
            preco=price,
        )

        if resultado:
            exibir_resultado_ordem(resultado)

    except Exception as e:
        click.echo(f"Falha ao enviar ordem: {e}")
