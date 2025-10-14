import click
import MetaTrader5 as mt5
from mtcli_trade.conf import DIGITOS


def exibir_ordens(ordens, symbol=None):
    if not ordens:
        click.echo(
            f"Nenhuma ordem pendente para {symbol}."
            if symbol
            else "Nenhuma ordem pendente encontrada."
        )
        return

    click.echo(f"Ordens pendentes{' para ' + symbol if symbol else ''}:\n")
    for o in ordens:
        click.echo(
            f"{o['tipo']} {o['symbol']} {o['volume']} {o['preco']} ticket {o['ticket']}"
        )


def exibir_cancelar_ordens(resultados, symbol=None):
    """Exibe os resultados dos cancelamentos de órdens."""
    if not resultados:
        click.echo(
            f"Nenhuma ordem pendente para {symbol}"
            if symbol
            else "Nenhuma ordem pendente encontrada"
        )
        return

    click.echo(f"Cancelando {len(resultados)} ordem(ns)...")

    for resultado in resultados:
        if resultado.retcode == mt5.TRADE_RETCODE_DONE:
            click.echo(f"Ordem cancelada {resultado.ticket} {resultado.symbol}")
        else:
            click.echo(
                f"Falha ao cancelar {resultado.ticket} código {resultado.retcode}"
            )
