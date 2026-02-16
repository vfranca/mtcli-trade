"""
Listener responsável por emitir sinal sonoro
em eventos relevantes.
"""

import sys
from ..events.event_bus import event_bus
from ..events.events import (
    POSITION_OPENED,
    POSITION_CLOSED,
)


def beep():
    """
    Emite beep simples compatível com terminal.
    """
    sys.stdout.write("\a")
    sys.stdout.flush()


def on_position_opened(**data):
    beep()


def on_position_closed(**data):
    beep()


# Registro automático ao importar
event_bus.subscribe(POSITION_OPENED, on_position_opened)
event_bus.subscribe(POSITION_CLOSED, on_position_closed)
