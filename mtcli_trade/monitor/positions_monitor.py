"""
Monitor contínuo de posições abertas.

Detecta:
- Nova posição aberta
- Posição fechada
"""

import time
from typing import Dict
from ..decorators.mt5_connection import with_mt5
from ..services.positions_service import buscar_posicoes_mt5
from ..events.event_bus import event_bus
from ..events.events import (
    POSITION_OPENED,
    POSITION_CLOSED,
)


class PositionsMonitor:
    """
    Monitor contínuo de posições abertas.
    """

    def __init__(self, symbol: str | None = None, interval: float = 1.0):
        self.symbol = symbol
        self.interval = interval
        self._snapshot: Dict[int, object] = {}

    @with_mt5
    def iniciar(self):
        """
        Inicia loop contínuo de monitoramento.
        """

        print("Monitor iniciado. Pressione Ctrl+C para sair.")

        # Snapshot inicial
        self._snapshot = self._obter_snapshot()

        try:
            while True:
                atual = self._obter_snapshot()

                self._detectar_novas(atual)
                self._detectar_fechadas(atual)

                self._snapshot = atual

                time.sleep(self.interval)

        except KeyboardInterrupt:
            print("\nMonitor finalizado.")

    def _obter_snapshot(self):
        """
        Retorna dict {ticket: posicao}
        """

        posicoes = buscar_posicoes_mt5(self.symbol) or []
        return {p.ticket: p for p in posicoes}

    def _detectar_novas(self, atual):
        """
        Detecta posições abertas após snapshot anterior.
        """

        novas = set(atual.keys()) - set(self._snapshot.keys())

        for ticket in novas:
            pos = atual[ticket]

            event_bus.publish(
                POSITION_OPENED,
                symbol=pos.symbol,
                ticket=pos.ticket,
                volume=pos.volume,
            )

            print(
                f"[OPEN] {pos.symbol} | "
                f"ticket {pos.ticket} | "
                f"vol {pos.volume}"
            )

    def _detectar_fechadas(self, atual):
        """
        Detecta posições fechadas após snapshot anterior.
        """

        fechadas = set(self._snapshot.keys()) - set(atual.keys())

        for ticket in fechadas:
            pos = self._snapshot[ticket]

            event_bus.publish(
                POSITION_CLOSED,
                symbol=pos.symbol,
                ticket=pos.ticket,
            )

            print(
                f"[CLOSE] {pos.symbol} | "
                f"ticket {pos.ticket}"
            )
