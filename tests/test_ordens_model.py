import pytest
from unittest.mock import patch, MagicMock
from mtcli_trade.models import ordens_model


@patch("mtcli_trade.models.ordens_model.mt5")
@patch("mtcli_trade.models.ordens_model.shutdown")
@patch("mtcli_trade.models.ordens_model.conectar")
def test_buscar_ordens_sem_symbol(mock_conectar, mock_shutdown, mock_mt5):
    mock_mt5.ordens_get.return_value = ["ordem1"]
    ordens = ordens_model.buscar_ordens()
    assert ordens == ["ordem1"]
    mock_conectar.assert_called_once()
    mock_shutdown.assert_called_once()


def test_formatar_ordem():
    ordem = MagicMock()
    ordem.type = 2
    ordem.symbol = "WIN"
    ordem.volume_current = 2.0
    ordem.price_open = 123456.789
    ordem.ticket = 9999

    result = ordens_model.formatar_ordem(ordem)
    assert result["tipo"] in ["COMPRA", "VENDA", "2"]
    assert result["symbol"] == "WIN"
    assert result["volume"] == 2.0
    assert "preco" in result
    assert result["ticket"] == 9999
