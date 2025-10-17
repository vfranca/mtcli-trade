import pytest
import time
from unittest.mock import patch, MagicMock
from mtcli_trade.controllers.compra_controller import executar_compra
from mtcli_trade.views.compra_view import exibir_resultado_compra
from mtcli_trade.commands.compra_cli import compra_cmd

# ==== INTEGRATION TESTS - CLI + PERFORMANCE ====
def test_cli_compra_sucesso(runner):
    with patch("mtcli_trade.commands.compra_cli.executar_compra") as mock_exec:
        mock_exec.return_value = {"status": "ok", "resultado": {"retcode": 10009}}
        start = time.perf_counter()
        result = runner.invoke(compra_cmd, ["--symbol", "WINV25", "--lot", "1.0"])
        duration = time.perf_counter() - start
        assert result.exit_code == 0
        assert "sucesso" in result.output.lower()
        assert duration < 0.5

def test_cli_compra_bloqueada(runner):
    with patch("mtcli_trade.commands.compra_cli.executar_compra") as mock_exec:
        mock_exec.return_value = {"status": "bloqueado"}
        start = time.perf_counter()
        result = runner.invoke(compra_cmd, ["--symbol", "WINV25"])
        duration = time.perf_counter() - start
        assert "bloqueada" in result.output.lower()
        assert duration < 0.5

def test_cli_compra_erro_preco_limit(runner):
    with patch("mtcli_trade.commands.compra_cli.executar_compra") as mock_exec:
        mock_exec.return_value = {"status": "erro", "mensagem": "Preço obrigatório"}
        start = time.perf_counter()
        result = runner.invoke(compra_cmd, ["--symbol", "WINV25", "--limit"])
        duration = time.perf_counter() - start
        assert "preço obrigatório" in result.output.lower()
        assert duration < 0.5

def test_cli_compra_falha_preparacao(runner):
    with patch("mtcli_trade.commands.compra_cli.executar_compra") as mock_exec:
        mock_exec.return_value = {"status": "falha"}
        start = time.perf_counter()
        result = runner.invoke(compra_cmd, ["--symbol", "WINV25"])
        duration = time.perf_counter() - start
        assert "falha" in result.output.lower()
        assert duration < 0.5

def test_cli_compra_desconhecido(runner):
    with patch("mtcli_trade.commands.compra_cli.executar_compra") as mock_exec:
        mock_exec.return_value = {"status": "xyz"}
        start = time.perf_counter()
        result = runner.invoke(compra_cmd, ["--symbol", "WINV25"])
        duration = time.perf_counter() - start
        assert "desconhecido" in result.output.lower()
        assert duration < 0.5
