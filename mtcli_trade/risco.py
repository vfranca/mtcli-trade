import MetaTrader5 as mt5

LIMITE_DIARIO = -180.00  # Ajuste o limite conforme desejado


def risco_excedido():
    info = mt5.account_info()
    if info is None:
        return False  # Se não for possível obter info, não bloqueia
    return info.profit <= LIMITE_DIARIO
