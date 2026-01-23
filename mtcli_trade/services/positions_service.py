import MetaTrader5 as mt5
from mtcli.conecta import conectar, shutdown


def buscar_posicoes_mt5(symbol=None):
    conectar()
    try:
        return mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()
    finally:
        shutdown()
