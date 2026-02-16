"""
Controller responsável por fechamento de posições.
Suporta fechamento por símbolo.
"""

import MetaTrader5 as mt5
from mtcli.logger import setup_logger
from ..decorators.mt5_connection import with_mt5
from ..services.positions_service import buscar_posicoes_mt5
from ..services.close_service import fechar_posicao_mt5
from ..events.event_bus import event_bus
from ..events.events import POSITION_CLOSED

log = setup_logger()


class CloseController:
    """
    Controller de fechamento de posições.
    """

    @with_mt5
    def fechar_por_symbol(self, symbol: str):
        """
        Fecha todas as posições abertas de um símbolo.
        """

        posicoes = buscar_posicoes_mt5(symbol)

        if not posicoes:
            log.info(f"Nenhuma posição aberta para {symbol}")
            return []

        resultados = []

        log.info(f"Iniciando fechamento de posições para {symbol}")

        for posicao in posicoes:

            resultado = fechar_posicao_mt5(
                symbol=posicao.symbol,
                ticket=posicao.ticket,
                volume=posicao.volume,
                tipo_posicao=posicao.type,
            )

            if resultado and resultado.retcode == mt5.TRADE_RETCODE_DONE:
                log.info(f"Fechado ticket {posicao.ticket}")

                event_bus.publish(
                    POSITION_CLOSED,
                    symbol=symbol,
                    ticket=posicao.ticket,
                )

            else:
                log.error(
                    f"Falha ao fechar ticket {posicao.ticket} | "
                    f"retcode={getattr(resultado, 'retcode', None)}"
                )

            resultados.append((posicao.ticket, resultado))

        log.info(
            f"Finalizado fechamento | {len(resultados)} tentativa(s)"
        )

        return resultados
