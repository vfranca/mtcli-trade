import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from mtcli_trade.controllers.venda_controller import executar_venda
from mtcli_trade.views.venda_view import exibir_resultado_venda

@pytest.fixture
def mock_venda_model(mocker):
    mocker.patch("mtcli_trade.models.venda_model.verificar_risco", return_value=False)
    mocker.patch("mtcli_trade.models.venda_model.preparar_ordem_venda", return_value=(MagicMock(), False))
    mocker.patch("mtcli_trade.models.venda_model.enviar_ordem_venda", return_value={"retcode": 10009})
    return mocker

def test_executar_venda_sucesso(mock_venda_model):
    resultado = executar_venda("WINV25", 1.0, 150, 300, False, None)
    assert resultado["status"] == "ok"
    assert "resultado" in resultado

def test_executar_venda_bloqueada(mocker):
    mocker.patch("mtcli_trade.models.venda_model.verificar_risco", return_value=True)
    resultado = executar_venda("WINV25", 1.0, 150, 300, False, None)
    assert resultado["status"] == "bloqueado"

def test_executar_venda_falha_preparacao(mocker):
    mocker.patch("mtcli_trade.models.venda_model.verificar_risco", return_value=False)
    mocker.patch("mtcli_trade.models.venda_model.preparar_ordem_venda", return_value=(None, False))
    resultado = executar_venda("WINV25", 1.0, 150, 300, False, None)
    assert resultado["status"] == "falha"

def test_executar_venda_valor_invalido(mocker):
    mocker.patch("mtcli_trade.models.venda_model.verificar_risco", return_value=False)
    mocker.patch("mtcli_trade.models.venda_model.preparar_ordem_venda", side_effect=ValueError("Preço obrigatório"))
    resultado = executar_venda("WINV25", 1.0, 150, 300, True, None)
    assert resultado["status"] == "erro"
    assert "Preço obrigatório" in resultado["mensagem"]

def test_executar_venda_excecao_inesperada(mocker):
    mocker.patch("mtcli_trade.models.venda_model.verificar_risco", return_value=False)
    mocker.patch("mtcli_trade.models.venda_model.preparar_ordem_venda", side_effect=RuntimeError("Erro MT5"))
    resultado = executar_venda("WINV25", 1.0, 150, 300, False, None)
    assert resultado["status"] == "erro"
    assert "Erro MT5" in resultado["mensagem"]

@pytest.mark.parametrize(
    "resultado, esperado",
    [
        ({"status": "bloqueado"}, "bloqueada"),
        ({"status": "falha"}, "Falha"),
        ({"status": "erro", "mensagem": "Erro interno"}, "Erro interno"),
        ({"status": "ok", "resultado": {"retcode": 10009}}, "sucesso"),
        ({"status": "desconhecido"}, "desconhecido"),
    ],
)
def test_exibir_resultado_venda_saida(resultado, esperado, capsys):
    exibir_resultado_venda(resultado)
    captured = capsys.readouterr()
    assert esperado.lower() in captured.out.lower()
