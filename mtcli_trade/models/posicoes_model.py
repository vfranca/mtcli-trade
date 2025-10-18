import MetaTrader5 as mt5
from mtcli_trade.logger import setup_logger
from mtcli_trade.mt5_context import mt5_conexao
from mtcli_trade.conf import LOSS_LIMIT, STATUS_FILE
from mtcli_trade.models.risco_model import controlar_risco
from mtcli_trade.models.ordem_model import criar_ordem, enviar_ordem

log = setup_logger()


def buscar_posicoes():
    """Retorna todas as posições abertas."""
    with mt5_conexao():
        return mt5.positions_get()


def encerra_posicoes():
    """Encerra todas as posições abertas."""
    resultados = []
    with mt5_conexao():
        posicoes = mt5.positions_get()

        if not posicoes:
            log.info("Nenhuma posição aberta encontrada.")
            return resultados

        for p in posicoes:
            tick = mt5.symbol_info_tick(p.symbol)
            if not tick:
                log.error(f"Falha ao obter tick para {p.symbol}")
                continue

            # Define tipo da operação inversa (encerramento)
            if p.type == mt5.POSITION_TYPE_BUY:
                tipo_ordem = mt5.ORDER_TYPE_SELL
                preco = tick.bid
            else:
                tipo_ordem = mt5.ORDER_TYPE_BUY
                preco = tick.ask

            ordem = criar_ordem(
                symbol=p.symbol,
                lot=p.volume,
                sl=0,
                tp=0,
                price=preco,
                order_type=tipo_ordem,
                limit=False,
            )

            resultado = enviar_ordem(ordem, limit=False)
            resultados.append(resultado)

            # ✅ Verificação de sucesso tolerante (mock + real)
            retcode = getattr(resultado, "retcode", None)
            if retcode in (mt5.TRADE_RETCODE_DONE, 10009):
                log.info(f"Posição {p.ticket} ({p.symbol}) encerrada com sucesso.")
            else:
                log.error(
                    f"Falha ao encerrar {p.symbol} (ticket {p.ticket}): retcode={retcode}"
                )

    return resultados


def editar_posicao(ticket, sl=None, tp=None):
    """Edita stop loss ou take profit de uma posição existente."""
    with mt5_conexao():
        posicoes = mt5.positions_get()
        if not posicoes:
            log.warning("Nenhuma posição encontrada para editar.")
            return False

        posicao = next((p for p in posicoes if p.ticket == ticket), None)
        if not posicao:
            log.error(f"Posição com ticket {ticket} não encontrada.")
            return False

        requisicao = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": posicao.ticket,
            "symbol": posicao.symbol,
            "sl": sl or posicao.sl,
            "tp": tp or posicao.tp,
        }

        resultado = mt5.order_send(requisicao)

        if resultado.retcode == mt5.TRADE_RETCODE_DONE:
            log.info(f"Posição {ticket} editada com sucesso.")
            return True
        else:
            log.error(f"Falha ao editar posição {ticket}: retcode={resultado.retcode}")
            return False


def verificar_risco_diario():
    """Executa controle de risco diário."""
    if controlar_risco(STATUS_FILE, LOSS_LIMIT):
        log.warning("Operações bloqueadas: limite de prejuízo diário atingido.")
        return True
    return False
