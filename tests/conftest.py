import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def mock_mt5(monkeypatch):
    """
    Mock global do módulo MetaTrader5 usado em mtcli_trade.
    Evita chamadas reais à API e fornece dados simulados.
    """

    mock_mt5 = MagicMock(name="MetaTrader5")

    # --- Constantes simuladas ---
    mock_mt5.ORDER_TYPE_BUY = 0
    mock_mt5.ORDER_TYPE_BUY_LIMIT = 2
    mock_mt5.ORDER_TIME_DAY = 1
    mock_mt5.ORDER_FILLING_IOC = 1
    mock_mt5.TRADE_ACTION_DEAL = 1
    mock_mt5.TRADE_ACTION_PENDING = 5
    mock_mt5.TRADE_RETCODE_DONE = 0
    mock_mt5.TRADE_RETCODE_PLACED = 10009

    # --- Métodos simulados ---
    mock_tick = MagicMock()
    mock_tick.ask = 125000.0
    mock_mt5.symbol_info_tick.return_value = mock_tick
    mock_mt5.symbol_info.return_value = MagicMock(point=0.01)
    mock_mt5.symbol_select.return_value = True

    mock_result = MagicMock()
    mock_result.retcode = mock_mt5.TRADE_RETCODE_DONE
    mock_result.comment = "Ordem executada"
    mock_result.price = 125000.0
    mock_mt5.order_send.return_value = mock_result

    # --- Substitui o módulo real MetaTrader5 por este mock ---
    monkeypatch.setattr("mtcli_trade.models.compra_model.mt5", mock_mt5)

    yield mock_mt5


@pytest.fixture(autouse=True)
def mock_mt5_conexao(monkeypatch):
    """
    Mock do contexto mt5_conexao usado em mtcli_trade.mt5_context.
    Evita conexão real com o terminal MT5.
    """

    class DummyConexao:
        def __enter__(self):
            return True

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    monkeypatch.setattr("mtcli_trade.models.compra_model.mt5_conexao", DummyConexao)
    yield
