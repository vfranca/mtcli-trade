import pytest
import time
from unittest.mock import patch
from mtcli_trade.commands.venda_cli import venda_cmd


def test_cli_venda_sucesso(runner):
    """Simula venda a mercado bem-sucedida."""
    with patch("mtcli_trade.commands.venda_cli.executar_venda") as mock_exec:
        mock_exec.return_value = {"status": "ok", "resultado": {"retcode": 10009}}
        start = time.perf_counter()
        result = runner.invoke(venda_cmd, ["--symbol", "WINV25", "--lot", "1.0"])
        duration = time.perf_counter() - start
        assert result.exit_code == 0
        assert "sucesso" in result.output.lower()
        assert duration < 0.5, f"Execução muito lenta: {duration:.3f}s"
        mock_exec.assert_called_once()


def test_cli_venda_bloqueada(runner):
    """Simula bloqueio por risco diário."""
    with patch("mtcli_trade.commands.venda_cli.executar_venda") as mock_exec:
        mock_exec.return_value = {"status": "bloqueado"}
        start = time.perf_counter()
        result = runner.invoke(venda_cmd, ["--symbol", "WINV25"])
        duration = time.perf_counter() - start
        assert "bloqueada" in result.output.lower()
        assert duration < 0.5


def test_cli_venda_erro_preco_limit(runner):
    """Simula erro ao tentar enviar ordem limit sem preço."""
    with patch("mtcli_trade.commands.venda_cli.executar_venda") as mock_exec:
        mock_exec.return_value = {"status": "erro", "mensagem": "Preço obrigatório"}
        start = time.perf_counter()
        result = runner.invoke(venda_cmd, ["--symbol", "WINV25", "--limit"])
        duration = time.perf_counter() - start
        assert "preço obrigatório" in result.output.lower()
        assert duration < 0.5


def test_cli_venda_falha_preparacao(runner):
    """Simula falha genérica ao preparar ordem."""
    with patch("mtcli_trade.commands.venda_cli.executar_venda") as mock_exec:
        mock_exec.return_value = {"status": "falha"}
        start = time.perf_counter()
        result = runner.invoke(venda_cmd, ["--symbol", "WINV25"])
        duration = time.perf_counter() - start
        assert "falha" in result.output.lower()
        assert duration < 0.5


def test_cli_venda_desconhecido(runner):
    """Simula retorno inesperado do controller."""
    with patch("mtcli_trade.commands.venda_cli.executar_venda") as mock_exec:
        mock_exec.return_value = {"status": "xyz"}
        start = time.perf_counter()
        result = runner.invoke(venda_cmd, ["--symbol", "WINV25"])
        duration = time.perf_counter() - start
        assert "desconhecido" in result.output.lower()
        assert duration < 0.5
