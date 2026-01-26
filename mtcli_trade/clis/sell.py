"""
Comando de envio de ordens de VENDA.
"""

import click
from ..controllers.sell_controller import SellController
from ..views.order_view import exibir_resultado_ordem
from ..conf import SYMBOL, LOT, SL, TP


@click.command()
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
    help="Envia ordem limitada (SELL LIMIT)."
)
@click.option(
    "--stop", "-st",
    is_flag=True,
    help="Envia ordem stop (SELL STOP)."
)
@click.option(
    "--preco", "-p",
    type=float,
    help="Preço de entrada para ordem pendente."
)
def sell(symbol, lot, sl, tp, limit, stop, preco):
    """
    Envia ordem de VENDA (market, limit ou stop).
    """
    controller = SellController()

    try:
        resultado = controller.executar(
            symbol=symbol,
            lot=lot,
            sl=sl,
            tp=tp,
            limit=limit,
            stop=stop,
            preco=preco,
        )

        if resultado:
            exibir_resultado_ordem(resultado)

    except Exception as e:
        click.echo(f"Falha ao enviar ordem de venda: {e}")
