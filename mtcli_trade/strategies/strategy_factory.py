"""
Factory para seleção da Strategy.
"""

from .market_strategy import MarketStrategy
from .limit_strategy import LimitStrategy
from .stop_strategy import StopStrategy


class StrategyFactory:

    @staticmethod
    def create(limit: bool, stop: bool):
        if limit and stop:
            raise ValueError("Não é possível usar --limit e --stop juntos.")

        if limit:
            return LimitStrategy()

        if stop:
            return StopStrategy()

        return MarketStrategy()
