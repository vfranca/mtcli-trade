"""
Serviço de acesso às ordens pendentes via MT5.
"""

import MetaTrader5 as mt5
from mtcli.conecta import conectar, shutdown


def buscar_ordens_mt5(symbol=None):
    conectar()
    try:
        return mt5.orders_get(symbol=symbol) if symbol else mt5.orders_get()
    finally:
        shutdown()
