"""
Controller responsável por fechamento de posições.
Suporta fechamento por símbolo.
"""

from mtcli.logger import setup_logger
from ..decorators.mt5_connection import with_mt5
from ..services.positions_service import buscar_posicoes_mt5
from ..services.close_service import fechar_posicao_mt5

log = setup_logger()


class CloseController:
    """
    Controller de fechamento de posições.
    """

    @with_mt5
    def fechar_por_symbol(self, symbol: str):
        """
        Fecha todas as posições abertas de um símbolo.

        :param symbol: código do ativo (ex: WIN, WDO, EURUSD)
        :return: lista de tuplas (ticket, resultado)
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

            if resultado and resultado.retcode == 10009:
                log.info(f"✔ Fechado ticket {posicao.ticket}")
            else:
                log.error(
                    f"✖ Falha ao fechar ticket {posicao.ticket} | "
                    f"retcode={getattr(resultado, 'retcode', None)}"
                )

            resultados.append((posicao.ticket, resultado))

        log.info(
            f"Finalizado fechamento | {len(resultados)} tentativa(s)"
        )

        return resultados
