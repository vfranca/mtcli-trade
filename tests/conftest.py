from unittest.mock import MagicMock, patch

from click.testing import CliRunner
import pytest


@pytest.fixture(autouse=True)
def mock_mt5():
    with patch("mtcli_trade.models.ordem_model.mt5") as mt5_mock:
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

        yield mt5_mock


@pytest.fixture
def mock_compra_model(mocker):
    mocker.patch("mtcli_trade.models.compra_model.verificar_risco", return_value=False)
    mocker.patch(
        "mtcli_trade.models.compra_model.preparar_ordem_compra",
        return_value=(MagicMock(), False),
    )
    mocker.patch(
        "mtcli_trade.models.compra_model.enviar_ordem_compra",
        return_value={"retcode": 10009},
    )
    return mocker


@pytest.fixture
def mock_venda_model(mocker):
    mocker.patch("mtcli_trade.models.venda_model.verificar_risco", return_value=False)
    mocker.patch(
        "mtcli_trade.models.venda_model.preparar_ordem_venda",
        return_value=(MagicMock(), False),
    )
    mocker.patch(
        "mtcli_trade.models.venda_model.enviar_ordem_venda",
        return_value={"retcode": 10009},
    )
    return mocker


@pytest.fixture
def runner():
    return CliRunner()
