from mtcli_trade.ordem import criar_ordem, enviar_ordem
from unittest.mock import MagicMock

def test_criar_ordem_market(mock_mt5):
    ordem = criar_ordem("WINV25", 1.0, 150, 300, 123.45, mock_mt5.ORDER_TYPE_BUY, limit=False)
    assert ordem["type"] == mock_mt5.ORDER_TYPE_BUY
    assert ordem["volume"] == 1.0
    assert ordem["symbol"] == "WINV25"

def test_enviar_ordem_market(mock_mt5):
    # Simula retorno da ordem enviada
    fake_result = MagicMock()
    fake_result.retcode = mock_mt5.TRADE_RETCODE_DONE
    mock_mt5.order_send.return_value = fake_result

    ordem = criar_ordem("WINV25", 1.0, 150, 300, 123.45, mock_mt5.ORDER_TYPE_BUY, limit=False)
    result = enviar_ordem(ordem, limit=False)

    assert result.retcode == mock_mt5.TRADE_RETCODE_DONE
    mock_mt5.order_send.assert_called_once_with(ordem)
