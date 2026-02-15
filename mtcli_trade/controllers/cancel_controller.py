"""
Controller responsável por cancelar ordens pendentes.
"""

from mtcli.logger import setup_logger
from ..services.cancel_service import cancelar_ordem_mt5

log = setup_logger()


class CancelController:
    """
    Controller de cancelamento de ordens.
    """

    def cancelar(self, ticket: int):
        """
        Executa cancelamento da ordem.

        Args:
            ticket (int): Ticket da ordem.
        """

        try:
            resultado = cancelar_ordem_mt5(ticket)

            if resultado is None:
                log.error("Falha ao enviar requisição ao MT5.")
                return None

            if resultado.retcode != 10009:  # TRADE_RETCODE_DONE
                log.error(
                    f"Erro ao cancelar ordem | retcode={resultado.retcode}"
                )
                return resultado

            log.info(f"Ordem {ticket} cancelada com sucesso.")
            return resultado

        except Exception:
            log.exception("Erro inesperado ao cancelar ordem.")
            raise
