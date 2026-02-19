"""
Monitor contínuo com multi-alvos em R e stop diário opcional.
Versão resiliente para execução longa.
"""

import time
import MetaTrader5 as mt5
from typing import Dict, List, Set
from ..services.positions_service import buscar_posicoes_mt5
from ..services.close_service import fechar_posicao_mt5
from ..services.mt5_service import MT5Service


class PositionsMonitor:
    """
    Monitor contínuo de posições com:
    - Multi-alvos baseados em R
    - Parciais configuráveis
    - Stop diário automático
    - Resiliência a falhas de conexão
    """

    def __init__(
        self,
        symbol: str | None = None,
        interval: float = 1.0,
        targets: List[float] | None = None,
        partials: List[float] | None = None,
        daily_stop: float | None = None,
    ):
        self.symbol = symbol
        self.interval = interval
        self.targets = targets or [1.0]
        self.partials = partials or [0.5]
        self.daily_stop = daily_stop

        self._executados: Dict[int, Set[int]] = {}
        self._lucro_dia: float = 0.0

        self.mt5_service = MT5Service()

    # =====================================================
    # CICLO DE VIDA
    # =====================================================

    def iniciar(self):
        print("Iniciando conexão com MT5...")

        if not mt5.initialize():
            codigo, msg = mt5.last_error()
            raise RuntimeError(f"Falha ao conectar ao MT5 ({codigo}, {msg})")

        print("Monitor iniciado. Ctrl+C para sair.")

        try:
            while True:
                try:
                    self._ciclo_monitoramento()
                except Exception as e:
                    print(f"[ERRO MONITOR] {e}")

                time.sleep(self.interval)

        except KeyboardInterrupt:
            print("\nMonitor finalizado pelo usuário.")

        finally:
            print("Encerrando conexão MT5...")
            mt5.shutdown()

    # =====================================================
    # CICLO
    # =====================================================

    def _ciclo_monitoramento(self):
        posicoes = buscar_posicoes_mt5(self.symbol) or []

        self._atualizar_lucro_dia(posicoes)

        if self._atingiu_stop_diario():
            print("STOP DIÁRIO ATINGIDO. Encerrando monitor.")
            raise KeyboardInterrupt

        for pos in posicoes:
            self._verificar_alvos(pos)

    # =====================================================
    # LÓGICA DE ALVOS
    # =====================================================

    def _verificar_alvos(self, pos):

        if not pos.sl or pos.sl == 0:
            return

        if pos.ticket not in self._executados:
            self._executados[pos.ticket] = set()

        tick = self.mt5_service.obter_tick(pos.symbol)
        if not tick:
            return

        entrada = pos.price_open
        sl = pos.sl

        if pos.type == mt5.POSITION_TYPE_BUY:
            r = entrada - sl
            if r <= 0:
                return
            preco_atual = tick.bid

        elif pos.type == mt5.POSITION_TYPE_SELL:
            r = sl - entrada
            if r <= 0:
                return
            preco_atual = tick.ask

        else:
            return

        for idx, target in enumerate(self.targets):

            if idx in self._executados[pos.ticket]:
                continue

            if pos.type == mt5.POSITION_TYPE_BUY:
                alvo = entrada + (r * target)
                atingiu = preco_atual >= alvo
            else:
                alvo = entrada - (r * target)
                atingiu = preco_atual <= alvo

            if atingiu:
                self._executar_parcial(pos, idx)

    # =====================================================
    # EXECUÇÃO PARCIAL
    # =====================================================

    def _executar_parcial(self, pos, idx):

        percentual = self.partials[idx]

        info = mt5.symbol_info(pos.symbol)
        if not info:
            return

        volume_step = info.volume_step
        volume_parcial = pos.volume * percentual

        volume_parcial = round(
            max(volume_step, volume_parcial),
            2
        )

        if volume_parcial >= pos.volume:
            return

        print(
            f"[{self.targets[idx]}R] {pos.symbol} | "
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
            self._executados[pos.ticket].add(idx)

    # =====================================================
    # STOP DIÁRIO
    # =====================================================

    def _atualizar_lucro_dia(self, posicoes):
        self._lucro_dia = sum(p.profit for p in posicoes)

    def _atingiu_stop_diario(self):

        if self.daily_stop is None:
            return False

        return self._lucro_dia <= -abs(self.daily_stop)
