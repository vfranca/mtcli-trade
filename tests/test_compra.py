import pytest
import time
from unittest.mock import patch, MagicMock
from mtcli_trade.controllers.compra_controller import executar_compra
from mtcli_trade.views.compra_view import exibir_resultado_compra
from mtcli_trade.commands.compra_cli import compra_cmd


# ==== UNIT TESTS - CONTROLLER ====
def test_executar_compra_sucesso(mock_compra_model):
    resultado = executar_compra("WINV25", 1.0, 150, 300, False, None)
    assert resultado["status"] == "ok"
    assert "resultado" in resultado


def test_executar_compra_bloqueada(mocker):
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.verificar_risco", return_value=True
    )
    resultado = executar_compra("WINV25", 1.0, 150, 300, False, None)
    assert resultado["status"] == "bloqueado"


def test_executar_compra_falha_preparacao(mocker):
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.verificar_risco", return_value=False
    )
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.preparar_ordem_compra",
        return_value=(None, False),
    )
    resultado = executar_compra("WINV25", 1.0, 150, 300, False, None)
    assert resultado["status"] == "falha"


def test_executar_compra_valor_invalido(mocker):
    mocker.patch("mtcli_trade.models.compra_model.verificar_risco", return_value=False)
    mocker.patch(
        "mtcli_trade.models.compra_model.preparar_ordem_compra",
        side_effect=ValueError("Preço obrigatório"),
    )
    resultado = executar_compra("WINV25", 1.0, 150, 300, True, None)
    assert resultado["status"] == "erro"
    assert "Preço obrigatório" in resultado["mensagem"]


def test_executar_compra_excecao_inesperada(mocker):
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.verificar_risco", return_value=False
    )
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.preparar_ordem_compra",
        side_effect=RuntimeError("Erro MT5"),
    )
    resultado = executar_compra("WINV25", 1.0, 150, 300, False, None)
    assert resultado["status"] == "erro"
    assert "Erro MT5" in resultado["mensagem"]


# ==== UNIT TESTS - VIEW ====
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
def test_exibir_resultado_compra_saida(resultado, esperado, capsys):
    exibir_resultado_compra(resultado)
    captured = capsys.readouterr()
    assert esperado.lower() in captured.out.lower()
