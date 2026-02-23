"""
Listener responsável por emitir sinal sonoro
em eventos relevantes.
"""

import sys
from ..events.event_bus import event_bus
from ..events.events import (
    POSITION_OPENED,
    POSITION_CLOSED,
    TARGET_HIT,
    STOP_DAILY_HIT,
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


def on_target_hit(**data):
    beep()


def on_stop_daily_hit(**data):
    beep()


# Registro automático
event_bus.subscribe(POSITION_OPENED, on_position_opened)
event_bus.subscribe(POSITION_CLOSED, on_position_closed)
event_bus.subscribe(TARGET_HIT, on_target_hit)
event_bus.subscribe(STOP_DAILY_HIT, on_stop_daily_hit)
