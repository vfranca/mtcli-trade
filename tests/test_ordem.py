import MetaTrader5 as mt5
from unittest.mock import patch, MagicMock
from mtcli_trade.ordem import inicializar, criar_ordem


@patch("mtcli_trade.ordem.mt5.symbol_select", return_value=True)
@patch("mtcli_trade.ordem.mt5.symbol_info_tick")
def test_inicializar(mock_tick, mock_select):
    mock_tick.return_value = MagicMock(ask=100000)
    tick = inicializar("WINV25")
    assert tick is not None
    assert tick.ask == 100000


@patch("mtcli_trade.ordem.mt5.symbol_info")
def test_criar_ordem(mock_info):
    mock_info.return_value = MagicMock(point=5)
    ordem = criar_ordem(
        symbol="WINV25",
        lot=1.0,
        sl=150,
        tp=300,
        price=100000,
        order_type=mt5.ORDER_TYPE_BUY,
        limit=False
    )
    assert ordem["sl"] == 100000 - 150 * 5
    assert ordem["tp"] == 100000 + 300
    assert ordem["volume"] == 1.0


