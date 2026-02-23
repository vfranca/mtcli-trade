"""
Monitor contínuo com:
- Multi-alvos em R
- Parciais configuráveis
- Break-even automático
- Trailing stop após X R
- Stop diário persistente
- EventBus integrado
"""

import time
import MetaTrader5 as mt5
from typing import Dict, List, Set
from ..services.positions_service import buscar_posicoes_mt5
from ..services.close_service import fechar_posicao_mt5
from ..services.mt5_service import MT5Service
from ..models.risk_engine import RiskEngine
from ..events.event_bus import event_bus
from ..events.events import TARGET_HIT, STOP_DAILY_HIT, TRAILING_UPDATED


class PositionsMonitor:

    def __init__(
        self,
        symbol: str | None = None,
        interval: float = 1.0,
        targets: List[float] | None = None,
        partials: List[float] | None = None,
        daily_stop: float | None = None,
        trailing_after: float | None = 2.0,
        trailing_step_r: float = 0.5,
        break_even_on_first: bool = True,
    ):
        self.symbol = symbol
        self.interval = interval
        self.targets = targets or [1.0]
        self.partials = partials or [0.5]
        self.daily_stop = daily_stop
        self.trailing_after = trailing_after
        self.trailing_step_r = trailing_step_r
        self.break_even_on_first = break_even_on_first

        self._executados: Dict[int, Set[int]] = {}

        self.mt5_service = MT5Service()
        self.risk_engine = RiskEngine()

    # =====================================================

    def iniciar(self):

        print("Iniciando monitor...")

        if not mt5.initialize():
            codigo, msg = mt5.last_error()
            raise RuntimeError(f"Falha MT5 ({codigo}, {msg})")

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

    def _ciclo(self):

        posicoes = buscar_posicoes_mt5(self.symbol) or []

        self._limpar_tickets_encerrados(posicoes)

        lucro = sum(p.profit for p in posicoes)
        self.risk_engine.atualizar_lucro(lucro)

        if self.daily_stop and self.risk_engine.atingiu_stop(self.daily_stop):
            event_bus.publish(STOP_DAILY_HIT)
            raise KeyboardInterrupt

        for pos in posicoes:
            self._verificar_alvos(pos)

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

            percentual = (
                self.partials[idx]
                if idx < len(self.partials)
                else self.partials[-1]
            )

            if pos.type == mt5.POSITION_TYPE_BUY:
                alvo = entrada + (r * target)
                atingiu = preco_atual >= alvo
            else:
                alvo = entrada - (r * target)
                atingiu = preco_atual <= alvo

            if atingiu:
                self._executar_parcial(pos, idx, percentual)
                event_bus.publish(TARGET_HIT, ticket=pos.ticket, r=target)

                if idx == 0 and self.break_even_on_first:
                    self._mover_break_even(pos)

        self._aplicar_trailing(pos, entrada, r, preco_atual)

    # =====================================================

    def _executar_parcial(self, pos, idx, percentual):

        info = mt5.symbol_info(pos.symbol)
        if not info:
            return

        step = info.volume_step
        volume = (pos.volume * percentual // step) * step
        volume = round(volume, 2)

        if volume <= 0 or volume >= pos.volume:
            return

        fechar_posicao_mt5(
            symbol=pos.symbol,
            ticket=pos.ticket,
            volume=volume,
            tipo_posicao=pos.type,
        )

        self._executados[pos.ticket].add(idx)

    # =====================================================

    def _mover_break_even(self, pos):

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": pos.symbol,
            "position": pos.ticket,
            "sl": pos.price_open,
            "tp": pos.tp,
        }

        mt5.order_send(request)

    # =====================================================

    def _aplicar_trailing(self, pos, entrada, r, preco_atual):

        if not self.trailing_after:
            return

        if pos.type == mt5.POSITION_TYPE_BUY:
            ativado = preco_atual >= entrada + (r * self.trailing_after)
            if not ativado:
                return

            novo_sl = preco_atual - (r * self.trailing_step_r)
            if novo_sl <= pos.sl:
                return

        else:
            ativado = preco_atual <= entrada - (r * self.trailing_after)
            if not ativado:
                return

            novo_sl = preco_atual + (r * self.trailing_step_r)
            if novo_sl >= pos.sl:
                return

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": pos.symbol,
            "position": pos.ticket,
            "sl": novo_sl,
            "tp": pos.tp,
        }

        mt5.order_send(request)
        event_bus.publish(TRAILING_UPDATED, ticket=pos.ticket)

    # =====================================================

    def _limpar_tickets_encerrados(self, posicoes):

        abertos = {p.ticket for p in posicoes}

        for ticket in list(self._executados.keys()):
            if ticket not in abertos:
                del self._executados[ticket]
