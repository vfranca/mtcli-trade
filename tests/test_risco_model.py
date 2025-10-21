from datetime import date
from unittest.mock import ANY, patch

from mtcli_trade.models.risco_model import controlar_risco


@patch("mtcli_trade.models.risco_model.carregar_estado")
@patch("mtcli_trade.models.risco_model.salvar_estado")
@patch("mtcli_trade.models.risco_model.risco_excedido", return_value=True)
@patch("mtcli_trade.models.risco_model.encerrar_todas_posicoes")
@patch("mtcli_trade.models.risco_model.cancelar_todas_ordens")
def test_controlar_risco_limite_excedido(
    mock_cancelar,
    mock_encerrar,
    mock_risco_excedido,
    mock_salvar_estado,
    mock_carregar_estado,
    caplog,
):
    mock_carregar_estado.return_value = {"data": "2020-01-01", "bloqueado": False}

    with caplog.at_level("INFO"):
        bloqueado = controlar_risco("estado.json", -100)

    assert bloqueado is True
    mock_encerrar.assert_called_once()
    mock_cancelar.assert_called_once()
    assert mock_salvar_estado.call_count == 2
    mock_salvar_estado.assert_any_call("estado.json", ANY, False)
    mock_salvar_estado.assert_any_call("estado.json", ANY, True)
    assert any("limite diário" in m.lower() for m in caplog.messages)


@patch("mtcli_trade.models.risco_model.carregar_estado")
@patch("mtcli_trade.models.risco_model.salvar_estado")
def test_controlar_risco_ja_bloqueado(mock_salvar_estado, mock_carregar_estado, caplog):
    mock_carregar_estado.return_value = {
        "data": date.today().isoformat(),
        "bloqueado": True,
    }

    with caplog.at_level("INFO"):
        bloqueado = controlar_risco("estado.json", -1000)

    assert bloqueado is True
    mock_salvar_estado.assert_not_called()
    assert any("bloqueado hoje por risco" in m.lower() for m in caplog.messages)


@patch("mtcli_trade.models.risco_model.carregar_estado")
@patch("mtcli_trade.models.risco_model.salvar_estado")
@patch("mtcli_trade.models.risco_model.risco_excedido", return_value=False)
def test_controlar_risco_dentro_do_limite(
    mock_risco_excedido,
    mock_salvar_estado,
    mock_carregar_estado,
):
    mock_carregar_estado.return_value = {
        "data": date.today().isoformat(),
        "bloqueado": False,
    }

    bloqueado = controlar_risco("estado.json", -1000)

    assert bloqueado is False
    mock_risco_excedido.assert_called_once()
