import click
import MetaTrader5 as mt5
from mtcli.conecta import conectar, shutdown
from mtcli.logger import setup_logger

logger = setup_logger("mt5")  # Cria o logger


@click.command()
@click.option(
    "--symbol", "-s", default="WINV25", help="Símbolo do ativo (default WINV25)."
)
@click.option(
    "--lot", "-l", type=float, default=1.0, help="Quantidade de contratos (default 1.0)"
)
@click.option(
    "-sl", type=float, default=150, help="Stop loss (em pontos) (default 150)"
)
@click.option(
    "-tp", type=float, default=300, help="Take profit (em pontos) (default 300)"
)
@click.option("--pendente", "-p", is_flag=True, help="Envia ordem pendente (buy limit)")
@click.option(
    "--preco", "-pr", type=float, default=None, help="Preço da ordem pendente"
)
def compra(symbol, lot, sl, tp, pendente, preco):
    """Compra a mercado ou pendente (buy limit) com SL e TP"""
    conectar()

    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        click.echo(f"❌ Erro: símbolo '{symbol}' não encontrado.")
        logger.info(f"Erro: símbolo '{symbol}' não encontrado.")
        shutdown()
        return

    if pendente:
        if preco is None:
            click.echo("❌ Para ordens pendentes, defina o --preco.")
            shutdown()
            return
        price = preco
        order_type = mt5.ORDER_TYPE_BUY_LIMIT
    else:
        price = tick.ask
        order_type = mt5.ORDER_TYPE_BUY

    sl_price = price - sl if sl > 0 else None
    tp_price = price + tp if tp > 0 else None

    logger.info(f"Enviando ordem de COMPRA {symbol} | lot: {lot} | SL: {sl} | TP: {tp}")
    logger.info(f"Preço atual: {price:.2f}")

    ordem = {
        "action": mt5.TRADE_ACTION_PENDING if pendente else mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl_price,
        "tp": tp_price,
        "deviation": 10,
        "magic": 1000,
        "comment": "Compra OCO",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    logger.info(f"Órdem enviada: {ordem}")

    resultado = mt5.order_send(ordem)
    if resultado.retcode == mt5.TRADE_RETCODE_DONE:
        click.echo(
            f"✅ Ordem {'pendente' if pendente else 'a mercado'} enviada com sucesso: ticket {resultado.order}"
        )
        logger.info(f"Ordem enviada com sucesso: ticket {resultado.order}")
    else:
        click.echo(f"❌ Falha ao enviar ordem: {resultado.retcode}")
        logger.error(f"Erro ao enviar ordem: retcode {resultado.retcode}.")

    shutdown()


if __name__ == "__main__":
    compra()
