"""risco.py - Controle automático de risco baseado no lucro/prejuízo da conta."""

import MetaTrader5 as mt5

# Limite diário configurável (ajustável via CLI ou .env futuramente)
LIMITE_DIARIO = -20.00


def risco_excedido(limite=LIMITE_DIARIO):
    """Retorna True se o prejuízo for igual ou maior que o limite diário."""
    info = mt5.account_info()
    if info is None:
        return False  # Em caso de falha ao obter info, não bloqueia por segurança
    return info.profit <= limite

