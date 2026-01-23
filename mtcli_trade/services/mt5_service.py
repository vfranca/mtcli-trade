"""
Serviços de integração com MetaTrader5.
"""

import MetaTrader5 as mt5
import click
from mtcli.conecta import conectar, shutdown
from mtcli.logger import setup_logger

log = setup_logger()


def obter_tick(symbol):
    conectar()
    if not mt5.symbol_select(symbol, True):
        shutdown()
        raise RuntimeError(f"Erro ao selecionar símbolo {symbol}")

    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        shutdown()
        raise RuntimeError(f"Erro ao obter tick de {symbol}")

    return tick


def enviar_ordem_mt5(ordem):
    log.info(f"Enviando ordem {ordem}")
    resultado = mt5.order_send(ordem)

    if resultado.retcode not in (
        mt5.TRADE_RETCODE_DONE,
        mt5.TRADE_RETCODE_PLACED,
    ):
        shutdown()
        raise RuntimeError(
            f"Falha no envio da ordem {resultado.retcode} - {resultado.comment}"
        )

    click.echo(f"Ordem enviada com sucesso | ticket {resultado.order}")
    shutdown()
    return resultado
