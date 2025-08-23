import click
import MetaTrader5 as mt5
from .conecta import conectar, shutdown
from .logger import setup_logger

logger = setup_logger("mt5")  # Cria o logger


@click.command()
@click.option("-s", "--symbol", default="WINV25", help="Símbolo do ativo")
@click.option("-l", "--lot", type=float, default=1.0, help="Quantidade de contratos")
@click.option("-sl", type=float, default=150, help="Stop loss (em pontos)")
@click.option("-tp", type=float, default=300, help="Take profit (em pontos)")
@click.option("--pendente", is_flag=True, help="Envia ordem pendente (sell limit)")
@click.option("--preco", type=float, default=None, help="Preço da ordem pendente")
def venda(symbol, lot, sl, tp, pendente, preco):
    """Venda a mercado ou pendente (sell limit) com SL e TP"""
    conectar()

    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        click.echo(f"❌ Erro: símbolo '{symbol}' não encontrado.")
        shutdown()
        return

    if pendente:
        if preco is None:
            click.echo("❌ Para ordens pendentes, defina o --preco.")
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
        "comment": "Venda OCO",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    resultado = mt5.order_send(ordem)
    if resultado.retcode == mt5.TRADE_RETCODE_DONE:
        click.echo(
            f"✅ Ordem {'pendente' if pendente else 'a mercado'} enviada com sucesso: ticket {resultado.order}"
        )
        logger.info(f"Ordem enviada com sucesso: ticket {resultado.order}")
    else:
        click.echo(f"❌ Falha ao enviar ordem: {resultado.retcode}")
        logger.error(f"Erro ao enviar ordem: retcode {resultado.retcode}")

    shutdown()
