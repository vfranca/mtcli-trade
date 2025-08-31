import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_mt5():
    with patch("mtcli_trade.ordem.mt5") as mt5:
        mt5.symbol_select.return_value = True
        mt5.symbol_info_tick.return_value = {"ask": 123.45}
        mt5.symbol_info.return_value = MagicMock(point=0.01)
        mt5.TRADE_RETCODE_DONE = 10009
        mt5.TRADE_RETCODE_PLACED = 10010
        mt5.ORDER_TYPE_BUY = 0
        mt5.ORDER_TYPE_BUY_LIMIT = 2
        mt5.TRADE_ACTION_DEAL = 1
        mt5.TRADE_ACTION_PENDING = 5
        mt5.ORDER_FILLING_IOC = 1
        mt5.ORDER_TIME_DAY = 1
        yield mt5
