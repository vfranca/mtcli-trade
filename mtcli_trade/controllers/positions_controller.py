"""
Controller de posições abertas.
"""

from mtcli.logger import setup_logger
from ..decorators.mt5_connection import with_mt5
from ..services.positions_service import buscar_posicoes_mt5
from ..models.positions_model import normalizar_posicao

log = setup_logger()


class PositionsController:
    """
    Controller responsável por posições abertas.
    """

    @with_mt5
    def obter_posicoes(
        self,
        symbol: str | None = None
    ) -> list[dict]:
        """
        Retorna lista de posições abertas normalizadas.
        """

        try:
            posicoes_raw = buscar_posicoes_mt5(symbol)

            if not posicoes_raw:
                self._log_sem_posicoes(symbol)
                return []

            posicoes = [
                normalizar_posicao(p)
                for p in posicoes_raw
            ]

            self._log_posicoes_encontradas(posicoes)

            return posicoes

        except Exception:
            log.exception("Erro ao obter posições abertas.")
            raise

    def calcular_resumo(self, posicoes: list[dict]) -> dict:
        """
        Calcula resumo consolidado das posições.
        """

        if not posicoes:
            return {}

        total_volume = sum(p["volume"] for p in posicoes)
        total_lucro = sum(p["lucro"] for p in posicoes)
        total_swap = sum(p["swap"] for p in posicoes)

        resumo = {
            "total_posicoes": len(posicoes),
            "volume_total": round(total_volume, 2),
            "lucro_total": round(total_lucro, 2),
            "swap_total": round(total_swap, 2),
        }

        log.info(
            f"Resumo | "
            f"posições={resumo['total_posicoes']} | "
            f"volume={resumo['volume_total']} | "
            f"lucro={resumo['lucro_total']}"
        )

        return resumo

    # ----------------------------------

    def _log_sem_posicoes(self, symbol):
        if symbol:
            log.info(f"Nenhuma posição aberta para {symbol}")
        else:
            log.info("Nenhuma posição aberta.")

    def _log_posicoes_encontradas(self, posicoes: list[dict]):
        log.info(f"{len(posicoes)} posição(ões) encontrada(s).")

        for p in posicoes:
            log.info(
                f"Ticket {p['ticket']} | "
                f"{p['tipo']} | "
                f"{p['symbol']} | "
                f"vol {p['volume']} | "
                f"lucro {p['lucro']}"
            )
