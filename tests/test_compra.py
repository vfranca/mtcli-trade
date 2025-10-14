import pytest
import time
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from mtcli_trade.controllers.compra_controller import executar_compra
from mtcli_trade.views.compra_view import exibir_resultado_compra
from mtcli_trade.commands.compra_cli import compra_cmd

# ==== UNIT TESTS - CONTROLLER ====
@pytest.fixture
def mock_compra_model(mocker):
    mocker.patch("mtcli_trade.models.compra_model.verificar_risco", return_value=False)
    mocker.patch("mtcli_trade.models.compra_model.preparar_ordem_compra", return_value=(MagicMock(), False))
    mocker.patch("mtcli_trade.models.compra_model.enviar_ordem_compra", return_value={"retcode": 10009})
    return mocker

def test_executar_compra_sucesso(mock_compra_model):
    resultado = executar_compra("WINV25", 1.0, 150, 300, False, None)
    assert resultado["status"] == "ok"
    assert "resultado" in resultado

def test_executar_compra_bloqueada(mocker):
    mocker.patch("mtcli_trade.models.compra_model.verificar_risco", return_value=True)
    resultado = executar_compra("WINV25", 1.0, 150, 300, False, None)
    assert resultado["status"] == "bloqueado"

def test_executar_compra_falha_preparacao(mocker):
    mocker.patch("mtcli_trade.models.compra_model.verificar_risco", return_value=False)
    mocker.patch("mtcli_trade.models.compra_model.preparar_ordem_compra", return_value=(None, False))
    resultado = executar_compra("WINV25", 1.0, 150, 300, False, None)
    assert resultado["status"] == "falha"

def test_executar_compra_valor_invalido(mocker):
    mocker.patch("mtcli_trade.models.compra_model.verificar_risco", return_value=False)
    mocker.patch("mtcli_trade.models.compra_model.preparar_ordem_compra", side_effect=ValueError("Preço obrigatório"))
    resultado = executar_compra("WINV25", 1.0, 150, 300, True, None)
    assert resultado["status"] == "erro"
    assert "Preço obrigatório" in resultado["mensagem"]

def test_executar_compra_excecao_inesperada(mocker):
    mocker.patch("mtcli_trade.models.compra_model.verificar_risco", return_value=False)
    mocker.patch("mtcli_trade.models.compra_model.preparar_ordem_compra", side_effect=RuntimeError("Erro MT5"))
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

# ==== INTEGRATION TESTS - CLI + PERFORMANCE ====
@pytest.fixture
def runner():
    return CliRunner()

def test_cli_compra_sucesso(runner):
    with patch("mtcli_trade.controllers.compra_controller.executar_compra") as mock_exec:
        mock_exec.return_value = {"status": "ok", "resultado": {"retcode": 10009}}
        start = time.perf_counter()
        result = runner.invoke(compra_cmd, ["--symbol", "WINV25", "--lot", "1.0"])
        duration = time.perf_counter() - start
        assert result.exit_code == 0
        assert "sucesso" in result.output.lower()
        assert duration < 0.5

def test_cli_compra_bloqueada(runner):
    with patch("mtcli_trade.controllers.compra_controller.executar_compra") as mock_exec:
        mock_exec.return_value = {"status": "bloqueado"}
        start = time.perf_counter()
        result = runner.invoke(compra_cmd, ["--symbol", "WINV25"])
        duration = time.perf_counter() - start
        assert "bloqueada" in result.output.lower()
        assert duration < 0.5

def test_cli_compra_erro_preco_limit(runner):
    with patch("mtcli_trade.controllers.compra_controller.executar_compra") as mock_exec:
        mock_exec.return_value = {"status": "erro", "mensagem": "Preço obrigatório"}
        start = time.perf_counter()
        result = runner.invoke(compra_cmd, ["--symbol", "WINV25", "--limit"])
        duration = time.perf_counter() - start
        assert "preço obrigatório" in result.output.lower()
        assert duration < 0.5

def test_cli_compra_falha_preparacao(runner):
    with patch("mtcli_trade.controllers.compra_controller.executar_compra") as mock_exec:
        mock_exec.return_value = {"status": "falha"}
        start = time.perf_counter()
        result = runner.invoke(compra_cmd, ["--symbol", "WINV25"])
        duration = time.perf_counter() - start
        assert "falha" in result.output.lower()
        assert duration < 0.5

def test_cli_compra_desconhecido(runner):
    with patch("mtcli_trade.controllers.compra_controller.executar_compra") as mock_exec:
        mock_exec.return_value = {"status": "xyz"}
        start = time.perf_counter()
        result = runner.invoke(compra_cmd, ["--symbol", "WINV25"])
        duration = time.perf_counter() - start
        assert "desconhecido" in result.output.lower()
        assert duration < 0.5
