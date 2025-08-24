import click
import MetaTrader5 as mt5
from mtcli.conecta import conectar, shutdown


@click.command()
@click.option("-s", "--symbol", default=None, help="Símbolo do ativo (opcional)")
def cancela(symbol):
    """Cancela todas as ordens pendentes (ou de um símbolo específico)"""
    conectar()

    ordens = mt5.orders_get(symbol=symbol) if symbol else mt5.orders_get()

    if not ordens:
        msg = (
            f"Nenhuma ordem pendente para {symbol}."
            if symbol
            else "Nenhuma ordem pendente encontrada."
        )
        click.echo(f"📭 {msg}")
        shutdown()
        return

    click.echo(f"📋 Cancelando {len(ordens)} ordem(ns)...")

    for ordem in ordens:
        req = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": ordem.ticket,
            "symbol": ordem.symbol,
            "magic": 1000,
            "comment": "Cancelamento via CLI",
        }

        res = mt5.order_send(req)
        if res.retcode == mt5.TRADE_RETCODE_DONE:
            click.echo(f"✅ Ordem cancelada: ticket {ordem.ticket} ({ordem.symbol})")
        else:
            click.echo(f"❌ Falha ao cancelar {ordem.ticket}: código {res.retcode}")

    shutdown()
