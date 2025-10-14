import MetaTrader5 as mt5
from mtcli.logger import setup_logger
from mtcli_trade.mt5_context import mt5_conexao
from typing import Optional, List, Any
import logging

log = setup_logger()


def buscar_posicoes(symbol: Optional[str] = None):
    """Retorna as posições abertas totais ou para um símbolo específico."""
    with mt5_conexao():
        return mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()


def editar_posicao(
    ticket: int, novo_sl: Optional[float] = None, novo_tp: Optional[float] = None
) -> Any:
    """Edita o stop loss e/ou take profit de uma posição aberta."""
    with mt5_conexao():
        posicao = mt5.positions_get(ticket=ticket)
        if not posicao:
            log.error(f"Posição com ticket {ticket} não encontrada")
            raise ValueError(f"Posição com ticket {ticket} não encontrada")

        pos = posicao[0]
        sl_val = novo_sl if novo_sl is not None else getattr(pos, "sl", 0.0)
        tp_val = novo_tp if novo_tp is not None else getattr(pos, "tp", 0.0)

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": int(ticket),
            "sl": float(sl_val),
            "tp": float(tp_val),
            "symbol": pos.symbol,
            "magic": getattr(pos, "magic", 0),
            "comment": "Editar SL/TP via mtcli-trade",
        }

        log.debug(f"Requisição SLTP: {request}")
        resultado = mt5.order_send(request)

        if resultado is None:
            log.error("order_send retornou None ao tentar editar SL/TP")
            raise RuntimeError("Falha na comunicação com MetaTrader5 ao editar SL/TP")

        if getattr(resultado, "retcode", None) != mt5.TRADE_RETCODE_DONE:
            log.error(
                f"Falha ao editar posição {ticket}: retcode={getattr(resultado, 'retcode', None)}"
            )
            raise RuntimeError(
                f"Falha ao editar posição {ticket}: {getattr(resultado, 'retcode', None)}"
            )

        log.info(f"Posição {ticket} editada com SL={sl_val} TP={tp_val}")
        return resultado


def encerra_posicoes(symbol: Optional[str] = None) -> List[Any]:
    """Encerra todas as posições abertas (ou de um símbolo)."""
    resultados = []
    with mt5_conexao():
        posicoes = mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()

        if not posicoes:
            log.info("Nenhuma posição aberta encontrada para encerrar.")
            return resultados

        for p in posicoes:
            tick = mt5.symbol_info_tick(p.symbol)
            if tick is None:
                log.error(
                    f"Não foi possível recuperar ticks para símbolo {p.symbol}. Pulando."
                )
                continue

            tipo_ordem = (
                mt5.ORDER_TYPE_SELL
                if p.type == mt5.POSITION_TYPE_BUY
                else mt5.ORDER_TYPE_BUY
            )
            price = tick.bid if p.type == mt5.POSITION_TYPE_BUY else tick.ask

            ordem = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": p.symbol,
                "volume": float(p.volume),
                "type": tipo_ordem,
                "price": float(price),
                "deviation": 10,
                "magic": getattr(p, "magic", 0),
                "comment": "Zerar posição",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            log.debug(f"Requisição para zerar posição (ticket {p.ticket}): {ordem}")
            resultado = mt5.order_send(ordem)

            if resultado is None:
                log.error(
                    f"order_send retornou None ao tentar zerar posição {p.ticket} ({p.symbol})"
                )
            elif getattr(resultado, "retcode", None) == mt5.TRADE_RETCODE_DONE:
                log.info(f"Posição {p.ticket} ({p.symbol}) encerrada com sucesso.")
            else:
                log.error(
                    f"Falha ao encerrar {p.symbol} (ticket {p.ticket}): retcode={getattr(resultado, 'retcode', None)}"
                )

            resultados.append(resultado)

    return resultados
