import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def mock_mt5():
    with patch("mtcli_trade.ordem.mt5") as mt5_mock, \
         patch("mtcli_trade.risco.mt5") as mt5_risco_mock:

        # Configuração simulada da API MT5
        mt5_mock.symbol_select.return_value = True
        mt5_mock.symbol_info_tick.return_value = MagicMock(ask=123.45)
        mt5_mock.symbol_info.return_value = MagicMock(point=0.01)
        mt5_mock.order_send.return_value = MagicMock(retcode=10009)
        mt5_mock.ORDER_TYPE_BUY = 0
        mt5_mock.ORDER_TYPE_BUY_LIMIT = 2
        mt5_mock.TRADE_ACTION_DEAL = 1
        mt5_mock.TRADE_ACTION_PENDING = 5
        mt5_mock.ORDER_FILLING_IOC = 1
        mt5_mock.ORDER_TIME_DAY = 1
        mt5_mock.TRADE_RETCODE_DONE = 10009
        mt5_mock.TRADE_RETCODE_PLACED = 10010

        mt5_risco_mock.account_info.return_value = MagicMock(profit=-200.0)

        yield mt5_mock
