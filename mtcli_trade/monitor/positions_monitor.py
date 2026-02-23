"""
Monitor contínuo com multi-alvos, break-even e stop diário.
Versão profissional resiliente.
"""

import time
import MetaTrader5 as mt5
from typing import Dict, List, Set
from ..services.positions_service import buscar_posicoes_mt5
from ..services.close_service import fechar_posicao_mt5
from ..services.mt5_service import MT5Service


class PositionsMonitor:

    def __init__(
        self,
        symbol: str | None = None,
        interval: float = 1.0,
        targets: List[float] | None = None,
        partials: List[float] | None = None,
        daily_stop: float | None = None,
        break_even_on_first: bool = True,
    ):
        self.symbol = symbol
        self.interval = interval
        self.targets = targets or [1.0]
        self.partials = partials or [0.5]
        self.daily_stop = daily_stop
        self.break_even_on_first = break_even_on_first

        self._executados: Dict[int, Set[int]] = {}
        self._lucro_dia: float = 0.0

        self.mt5_service = MT5Service()

    # =====================================================
    # CICLO
    # =====================================================

    def iniciar(self):

        print("Iniciando conexão MT5...")

        if not mt5.initialize():
            codigo, msg = mt5.last_error()
            raise RuntimeError(f"Falha MT5 ({codigo}, {msg})")

        print("Monitor ativo. Ctrl+C para sair.")

        try:
            while True:
                try:
                    self._ciclo()
                except Exception as e:
                    print(f"[ERRO MONITOR] {e}")

                time.sleep(self.interval)

        except KeyboardInterrupt:
            print("Monitor encerrado.")

        finally:
            mt5.shutdown()

    # =====================================================
    # LOOP
    # =====================================================

    def _ciclo(self):

        posicoes = buscar_posicoes_mt5(self.symbol) or []

        self._limpar_tickets_encerrados(posicoes)

        self._atualizar_lucro_dia(posicoes)

        if self._atingiu_stop_diario():
            print("STOP DIÁRIO ATINGIDO.")
            raise KeyboardInterrupt

        for pos in posicoes:
            self._verificar_alvos(pos)

    # =====================================================
    # LÓGICA R
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
            preco_atual = tick.bid
        else:
            r = sl - entrada
            preco_atual = tick.ask

        if r <= 0:
            return

        for idx, target in enumerate(self.targets):

            if idx in self._executados[pos.ticket]:
                continue

            percentual = self._obter_percentual(idx)

            if pos.type == mt5.POSITION_TYPE_BUY:
                alvo = entrada + (r * target)
                atingiu = preco_atual >= alvo
            else:
                alvo = entrada - (r * target)
                atingiu = preco_atual <= alvo

            if atingiu:
                self._executar_parcial(pos, idx, percentual)

                if idx == 0 and self.break_even_on_first:
                    self._mover_stop_break_even(pos)

    # =====================================================
    # PARCIAL
    # =====================================================

    def _executar_parcial(self, pos, idx, percentual):

        info = mt5.symbol_info(pos.symbol)
        if not info:
            return

        volume_step = info.volume_step
        volume_parcial = pos.volume * percentual

        # Ajuste correto ao step
        volume_parcial = (volume_parcial // volume_step) * volume_step
        volume_parcial = round(volume_parcial, 2)

        if volume_parcial <= 0:
            return

        if volume_parcial >= pos.volume:
            return

        print(
            f"ALVO {self.targets[idx]}R | "
            f"{pos.symbol} | "
            f"ticket {pos.ticket} | "
            f"volume {volume_parcial}"
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
    # BREAK EVEN
    # =====================================================

    def _mover_stop_break_even(self, pos):

        print(f"Movendo stop para BE | ticket {pos.ticket}")

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": pos.symbol,
            "position": pos.ticket,
            "sl": pos.price_open,
            "tp": pos.tp,
        }

        mt5.order_send(request)

    # =====================================================
    # STOP DIÁRIO
    # =====================================================

    def _atualizar_lucro_dia(self, posicoes):
        self._lucro_dia = sum(p.profit for p in posicoes)

    def _atingiu_stop_diario(self):

        if self.daily_stop is None:
            return False

        return self._lucro_dia <= -abs(self.daily_stop)

    # =====================================================
    # AUXILIARES
    # =====================================================

    def _obter_percentual(self, idx):

        if idx < len(self.partials):
            return self.partials[idx]

        return self.partials[-1]

    def _limpar_tickets_encerrados(self, posicoes):

        tickets_abertos = {p.ticket for p in posicoes}

        tickets_salvos = list(self._executados.keys())

        for ticket in tickets_salvos:
            if ticket not in tickets_abertos:
                del self._executados[ticket]
