"""
Decorator para abrir automaticamente conexão MT5
usando o context manager oficial do mtcli.
"""

from functools import wraps
from mtcli.mt5_context import mt5_conexao


def with_mt5(func):
    """
    Decorator que executa função dentro de
    um bloco mt5_conexao().

    Uso:

        @with_mt5
        def metodo(...):
            ...
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        with mt5_conexao():
            return func(*args, **kwargs)

    return wrapper
