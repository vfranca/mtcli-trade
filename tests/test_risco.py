from mtcli_trade import risco
from unittest.mock import MagicMock, patch

def test_risco_excedido_true():
    with patch("mtcli_trade.risco.mt5.account_info") as mock_info:
        mock_info.return_value = MagicMock(profit=-500.0)
        assert risco.risco_excedido() is True

def test_risco_excedido_false():
    with patch("mtcli_trade.risco.mt5.account_info") as mock_info:
        mock_info.return_value = MagicMock(profit=100.0)
        assert risco.risco_excedido() is False

