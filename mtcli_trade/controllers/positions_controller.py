"""
Controller de posições abertas.

Responsável por:
- Buscar posições via service
- Normalizar via model
- Registrar logs
- Retornar estrutura pronta para view
"""

from mtcli.logger import setup_logger
from ..services.positions_service import buscar_posicoes_mt5
from ..models.positions_model import normalizar_posicao

log = setup_logger()


class PositionsController:
    """
    Controller responsável por posições abertas.
    """

    def obter_posicoes(self, symbol: str | None = None) -> list[dict]:
        """
        Retorna lista de posições abertas normalizadas.

        :param symbol: ativo opcional
        :return: lista de dicionários
        """

        try:
            posicoes_raw = buscar_posicoes_mt5(symbol)

            if not posicoes_raw:
                self._log_sem_posicoes(symbol)
                return []

            posicoes = [normalizar_posicao(p) for p in posicoes_raw]

            self._log_posicoes_encontradas(posicoes)

            return posicoes

        except Exception:
            log.exception("Erro ao obter posições abertas.")
            raise

    # -------------------------
    # Métodos auxiliares
    # -------------------------

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
