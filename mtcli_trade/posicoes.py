import click
import MetaTrader5 as mt5
from .conecta import conectar, shutdown


@click.command()
@click.option("-s", "--symbol", default=None, help="Símbolo do ativo (opcional)")
def posicoes(symbol):
    """Lista todas as posições abertas (ou de um símbolo)"""
    conectar()

    posicoes = mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()

    if not posicoes:
        msg = (
            f"Nenhuma posição aberta para {symbol}."
            if symbol
            else "Nenhuma posição aberta encontrada."
        )
        click.echo(f"📭 {msg}")
        shutdown()
        return

    click.echo(f"📊 Posições abertas{' para ' + symbol if symbol else ''}:\n")
    for p in posicoes:
        tipo = "COMPRA" if p.type == mt5.POSITION_TYPE_BUY else "VENDA"
        click.echo(
            f"▶ {tipo} | {p.symbol} | volume: {p.volume:.2f} | preço: {p.price_open:.2f} | lucro: {p.profit:.2f}"
        )

    shutdown()
