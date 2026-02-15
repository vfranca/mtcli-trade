"""
Controller responsável por obter e processar ordens pendentes.
"""

from mtcli.logger import setup_logger
from ..decorators.mt5_connection import with_mt5
from ..services.orders_service import buscar_ordens_mt5
from ..models.orders_model import normalizar_ordem

log = setup_logger()


class OrdersController:
    """
    Controller de ordens pendentes.
    """

    @with_mt5
    def obter_ordens_pendentes(
        self,
        symbol: str | None = None
    ) -> list[dict]:
        """
        Retorna lista normalizada de ordens pendentes.
        """

        try:
            ordens_raw = buscar_ordens_mt5(symbol)

            if not ordens_raw:
                self._log_sem_ordens(symbol)
                return []

            ordens = [normalizar_ordem(o) for o in ordens_raw]

            self._log_ordens_encontradas(ordens)

            return ordens

        except Exception:
            log.exception("Erro ao obter ordens pendentes")
            raise

    # ----------------------------------

    def _log_sem_ordens(self, symbol):
        if symbol:
            log.info(f"Nenhuma ordem pendente para {symbol}")
        else:
            log.info("Nenhuma ordem pendente encontrada")

    def _log_ordens_encontradas(self, ordens: list[dict]):
        log.info(f"{len(ordens)} ordem(ns) pendente(s) encontrada(s)")

        for o in ordens:
            log.info(
                f"{o['tipo']} | {o['symbol']} | "
                f"vol {o['volume']} | "
                f"preço {o['preco']} | "
                f"ticket {o['ticket']}"
            )
