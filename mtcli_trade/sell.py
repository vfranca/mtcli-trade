import click
import MetaTrader5 as mt5
from . import conf
from mtcli.conecta import conectar, shutdown
from mtcli.logger import setup_logger

logger = setup_logger("trade")


@click.command()
@click.option(
    "--symbol", "-s", default="WINV25", help="Símbolo do ativo (default WINV25)."
)
@click.option(
    "--lot",
    type=float,
    default=1.0,
    help="Quantidade de contratos (default =1.0)",
)
@click.option(
    "-sl", type=float, default=150, help="Stop loss (em pontos) (default 150)."
)
@click.option("-tp", type=float, default=300, help="Take profit (em pontos)")
@click.option("--limit", "-l", is_flag=True, help="Envia ordem limit (sell limit)")
@click.option("--preco", "-pr", type=float, default=None, help="Preço da ordem limit")
def sell(symbol, lot, sl, tp, limit, preco):
    """Venda a mercado ou limit (sell limit) com sl e tp."""
    conectar()

    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        click.echo(f"❌ Erro: símbolo '{symbol}' não encontrado.")
        logger.error(f"Erro: símbolo '{symbol}' não encontrado")
        shutdown()
        return

    if limit:
        if preco is None:
            click.echo("❌ Para ordens pendente, defina o --preco.")
            logger.warning("Para ordens pendente, defina o --preco.")
            shutdown()
            return
        price = preco
        order_type = mt5.ORDER_TYPE_SELL_LIMIT
    else:
        price = tick.bid
        order_type = mt5.ORDER_TYPE_SELL

    sl_price = price + sl if sl > 0 else None
    tp_price = price - tp if tp > 0 else None

    logger.info(f"Enviando ordem de VENDA {symbol} | lot: {lot} | SL: {sl} | TP: {tp}")
    logger.info(f"Preço atual: {price:.{conf.digitos}f}")

    ordem = {
        "action": mt5.TRADE_ACTION_PENDING if limit else mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl_price,
        "tp": tp_price,
        "deviation": 10,
        "magic": 1000,
        "comment": "Venda OCO",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    logger.info(f"Órdem enviada: {ordem}")

    resultado = mt5.order_send(ordem)
    if resultado.retcode == mt5.TRADE_RETCODE_DONE:
        click.echo(
            f"Ordem {'limitada' if limit else 'a mercado'} enviada com sucesso: ticket {resultado.order}"
        )
        logger.info(
            f"Ordem {'limitada' if limit else 'a mercado'} enviada com sucesso: ticket {resultado.order}."
        )
    else:
        click.echo(f"❌ Falha ao enviar ordem: {resultado.retcode}")
        logger.error(f"Erro ao enviar ordem: retcode {resultado.retcode}")

    shutdown()


if __name__ == "__main__":
    sell()
