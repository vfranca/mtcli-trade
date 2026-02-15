"""
Controller responsável por cancelar ordens pendentes.
Suporta cancelamento unitário ou em massa.
"""

import MetaTrader5 as mt5
from mtcli.logger import setup_logger
from ..decorators.mt5_connection import with_mt5
from ..services.cancel_service import cancelar_ordem_mt5
from ..services.orders_service import buscar_ordens_mt5

log = setup_logger()


class CancelController:
    """
    Controller de cancelamento de ordens.
    """

    @with_mt5
    def cancelar_por_ticket(self, ticket: int):
        """
        Cancela uma ordem específica.
        """

        resultado = cancelar_ordem_mt5(ticket)

        if resultado is None:
            log.error("Falha ao enviar requisição ao MT5.")
            return None

        if resultado.retcode != mt5.TRADE_RETCODE_DONE:
            log.error(
                f"Erro ao cancelar ordem {ticket} | "
                f"retcode={resultado.retcode}"
            )
        else:
            log.info(f"Ordem {ticket} cancelada com sucesso.")

        return resultado

    @with_mt5
    def cancelar_por_symbol(self, symbol: str):
        """
        Cancela todas as ordens pendentes de um símbolo.
        """

        ordens = buscar_ordens_mt5(symbol)

        if not ordens:
            log.info(f"Nenhuma ordem pendente para {symbol}")
            return []

        resultados = []

        log.info(f"Iniciando cancelamento em massa para {symbol}")

        for ordem in ordens:
            ticket = ordem.ticket
            resultado = cancelar_ordem_mt5(ticket)

            if resultado and resultado.retcode == mt5.TRADE_RETCODE_DONE:
                log.info(f"✔ Cancelado ticket {ticket}")
            else:
                log.error(
                    f"✖ Falha ao cancelar ticket {ticket} | "
                    f"retcode={getattr(resultado, 'retcode', None)}"
                )

            resultados.append((ticket, resultado))

        log.info(
            f"Finalizado cancelamento em massa | "
            f"{len(resultados)} tentativa(s)"
        )

        return resultados
