"""
Monitor contínuo com realização parcial automática em 1R.
"""

import time
import MetaTrader5 as mt5
from typing import Set
from ..decorators.mt5_connection import with_mt5
from ..services.positions_service import buscar_posicoes_mt5
from ..services.close_service import fechar_posicao_mt5
from ..services.mt5_service import MT5Service


class PositionsMonitor:
    """
    Monitor contínuo de posições com parcial em 1R.
    """

    def __init__(
        self,
        symbol: str | None = None,
        interval: float = 1.0,
        parcial_percentual: float = 0.5,
    ):
        self.symbol = symbol
        self.interval = interval
        self.parcial_percentual = parcial_percentual
        self._realizadas: Set[int] = set()

        self.mt5_service = MT5Service()

    # -----------------------------------------------------

    @with_mt5
    def iniciar(self):
        print("Monitor iniciado (parcial 1R ativa). Ctrl+C para sair.")

        try:
            while True:
                posicoes = buscar_posicoes_mt5(self.symbol) or []

                for pos in posicoes:
                    self._verificar_parcial(pos)

                time.sleep(self.interval)

        except KeyboardInterrupt:
            print("\nMonitor finalizado.")

    # -----------------------------------------------------

    def _verificar_parcial(self, pos):

        if pos.ticket in self._realizadas:
            return

        if not pos.sl or pos.sl == 0:
            return  # Sem SL definido

        tick = self.mt5_service.obter_tick(pos.symbol)
        if not tick:
            return

        entrada = pos.price_open
        sl = pos.sl

        # ------------------------
        # BUY
        # ------------------------

        if pos.type == mt5.POSITION_TYPE_BUY:

            r = entrada - sl
            if r <= 0:
                return

            alvo_1r = entrada + r
            preco_atual = tick.bid

            if preco_atual >= alvo_1r:
                self._executar_parcial(pos)

        # ------------------------
        # SELL
        # ------------------------

        elif pos.type == mt5.POSITION_TYPE_SELL:

            r = sl - entrada
            if r <= 0:
                return

            alvo_1r = entrada - r
            preco_atual = tick.ask

            if preco_atual <= alvo_1r:
                self._executar_parcial(pos)

    # -----------------------------------------------------

    def _executar_parcial(self, pos):

        info = mt5.symbol_info(pos.symbol)
        if not info:
            return

        volume_step = info.volume_step

        volume_parcial = pos.volume * self.parcial_percentual

        # Ajusta para múltiplo válido
        volume_parcial = round(
            max(volume_step, volume_parcial),
            2
        )

        if volume_parcial >= pos.volume:
            return  # evita fechar tudo

        print(
            f"[PARCIAL 1R] {pos.symbol} | "
            f"ticket {pos.ticket} | "
            f"vol {volume_parcial}"
        )

        resultado = fechar_posicao_mt5(
            symbol=pos.symbol,
            ticket=pos.ticket,
            volume=volume_parcial,
            tipo_posicao=pos.type,
        )

        if resultado and resultado.retcode == mt5.TRADE_RETCODE_DONE:
            self._realizadas.add(pos.ticket)
