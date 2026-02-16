"""
EventBus simples síncrono para comunicação interna.
"""

from collections import defaultdict
from typing import Callable


class EventBus:
    """
    EventBus simples baseado em publish/subscribe.
    """

    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event_name: str, handler: Callable):
        """
        Registra um handler para um evento.
        """
        self._subscribers[event_name].append(handler)

    def publish(self, event_name: str, **data):
        """
        Publica evento e notifica handlers.
        """
        for handler in self._subscribers[event_name]:
            handler(**data)


# Instância global única
event_bus = EventBus()
