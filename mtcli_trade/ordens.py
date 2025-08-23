import click
import MetaTrader5 as mt5
from .conecta import conectar, shutdown


@click.command()
@click.option("-s", "--symbol", default=None, help="Símbolo do ativo (opcional)")
def ordens(symbol):
    """Lista todas as ordens pendentes (ou de um símbolo)"""
    conectar()

    if symbol:
        ordens = mt5.orders_get(symbol=symbol)
    else:
        ordens = mt5.orders_get()

    if not ordens:
        msg = (
            f"Nenhuma ordem pendente para {symbol}."
            if symbol
            else "Nenhuma ordem pendente encontrada."
        )
        click.echo(f"📭 {msg}")
        shutdown()
        return

    click.echo(f"📋 Ordens pendentes{' para ' + symbol if symbol else ''}:\n")
    for o in ordens:
        tipo = (
            "COMPRA"
            if o.type == mt5.ORDER_TYPE_BUY_LIMIT
            else "VENDA" if o.type == mt5.ORDER_TYPE_SELL_LIMIT else str(o.type)
        )
        click.echo(
            f"▶ {tipo} | {o.symbol} | volume: {o.volume_current} | preço: {o.price_open:.2f} | ticket: {o.ticket}"
        )

    shutdown()
