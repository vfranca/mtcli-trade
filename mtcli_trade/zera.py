import click
import MetaTrader5 as mt5
from mtcli.conecta import conectar, shutdown


@click.command()
@click.option("-s", "--symbol", default=None, help="Símbolo do ativo (opcional)")
def zera(symbol):
    """Encerra todas as posições abertas (ou de um símbolo)"""
    conectar()

    posicoes = mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()

    if not posicoes:
        msg = (
            f"Nenhuma posição para {symbol}."
            if symbol
            else "Nenhuma posição encontrada."
        )
        click.echo(f"📭 {msg}")
        shutdown()
        return

    for p in posicoes:
        ordem = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": p.symbol,
            "volume": p.volume,
            "type": (
                mt5.ORDER_TYPE_SELL
                if p.type == mt5.POSITION_TYPE_BUY
                else mt5.ORDER_TYPE_BUY
            ),
            "price": (
                mt5.symbol_info_tick(p.symbol).bid
                if p.type == mt5.POSITION_TYPE_BUY
                else mt5.symbol_info_tick(p.symbol).ask
            ),
            "deviation": 10,
            "magic": 1001,
            "comment": "Zerar posição",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        res = mt5.order_send(ordem)
        if res.retcode == mt5.TRADE_RETCODE_DONE:
            click.echo(f"✅ Posição {p.ticket} ({p.symbol}) encerrada.")
        else:
            click.echo(
                f"❌ Falha ao encerrar {p.symbol} (ticket {p.ticket}): {res.retcode}"
            )

    shutdown()
