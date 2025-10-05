from unittest.mock import patch, MagicMock
from mtcli_trade.controllers.orders_controller import obter_ordens_pendentes


@patch("mtcli_trade.controllers.orders_controller.formatar_ordem")
@patch("mtcli_trade.controllers.orders_controller.buscar_ordens")
def test_obter_ordens_pendentes_com_resultado(mock_buscar, mock_formatar):
    mock_ordem = MagicMock()
    mock_buscar.return_value = [mock_ordem]
    mock_formatar.return_value = {
        "tipo": "COMPRA",
        "symbol": "WIN",
        "volume": 1,
        "preco": 100,
        "ticket": 123,
    }

    resultado = obter_ordens_pendentes()
    assert isinstance(resultado, list)
    assert len(resultado) == 1
    assert resultado[0]["tipo"] == "COMPRA"


@patch("mtcli_trade.controllers.orders_controller.buscar_ordens")
def test_obter_ordens_pendentes_vazio(mock_buscar):
    mock_buscar.return_value = []
    resultado = obter_ordens_pendentes()
    assert resultado == []
