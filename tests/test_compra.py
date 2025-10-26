import pytest
from unittest.mock import patch
from click.testing import CliRunner

from mtcli_trade.controllers.compra_controller import processar_compra
from mtcli_trade.models import compra_model
from mtcli_trade.views.compra_view import exibir_compra
from mtcli_trade.commands.compra import compra  # caso o comando esteja registrado via entrypoint


# ============================================================
# 🧩 CENÁRIO 1 — Compra bem-sucedida
# ============================================================

@patch("mtcli_trade.models.compra_model.verificar_risco", return_value=None)
@patch("mtcli_trade.models.compra_model.enviar_compra")
def test_compra_sucesso(mock_enviar, mock_risco):
    mock_enviar.return_value = {
        "status": "sucesso",
        "codigo": 0,
        "mensagem": "Compra executada com sucesso",
        "preco": 125000.0,
    }

    res = processar_compra("WINZ25", 1, 150, 300, False, None)

    assert res["status"] == "sucesso"
    assert res["codigo"] == 0
    assert "sucesso" in res["mensagem"].lower()
    assert res["preco"] == 125000.0


# ============================================================
# 🚫 CENÁRIO 2 — Bloqueio de risco diário
# ============================================================

@patch("mtcli_trade.models.compra_model.verificar_risco")
def test_compra_bloqueada(mock_risco):
    mock_risco.return_value = {
        "status": "bloqueado",
        "codigo": -1,
        "mensagem": "Ordem bloqueada: limite de prejuízo diário atingido",
        "preco": 0.00,
    }

    res = processar_compra("WINZ25", 1, 150, 300, False, None)

    assert res["status"] == "bloqueado"
    assert res["codigo"] == -1
    assert "bloqueada" in res["mensagem"].lower()


# ============================================================
# ⚠️ CENÁRIO 3 — Falha de preço ausente em ordem pendente
# ============================================================

@patch("mtcli_trade.models.compra_model.verificar_risco", return_value=None)
def test_erro_preco_pendente(mock_risco):
    with patch("mtcli_trade.models.compra_model.enviar_compra") as mock_enviar:
        mock_enviar.return_value = {
            "status": "falha",
            "codigo": -1,
            "mensagem": "Para ordens pendentes, defina o --preco",
            "preco": 0.00,
        }

        res = processar_compra("WINZ25", 1, 150, 300, True, None)

        assert res["status"] == "falha"
        assert res["codigo"] == -1
        assert "preco" in res["mensagem"].lower()


# ============================================================
# 💣 CENÁRIO 4 — Falha inesperada (ex: erro MT5)
# ============================================================

@patch("mtcli_trade.models.compra_model.verificar_risco", return_value=None)
def test_falha_envio(mock_risco):
    with patch("mtcli_trade.models.compra_model.enviar_compra") as mock_enviar:
        mock_enviar.side_effect = Exception("Falha na conexão com MT5")

        res = processar_compra("WINZ25", 1, 150, 300, False, None)

        assert res["status"] == "erro"
        assert res["codigo"] == -1
        assert "falha" in res["mensagem"].lower() or "erro" in res["mensagem"].lower()


# ============================================================
# 🖥️ CENÁRIO 5 — Teste da VIEW (exibir_compra)
# ============================================================

def test_exibir_compra_saida(capsys):
    resultado = {
        "status": "sucesso",
        "codigo": 0,
        "mensagem": "Compra executada",
        "preco": 123456.78,
    }

    exibir_compra(resultado)
    saida = capsys.readouterr().out

    assert "Resultado da compra" in saida
    assert "sucesso" in saida
    assert "123456.78" in saida


# ============================================================
# 💻 CENÁRIO 6 — Teste do comando CLI (Click)
# ============================================================

@patch("mtcli_trade.controllers.compra_controller.processar_compra")
def test_cli_compra_sucesso(mock_processar):
    mock_processar.return_value = {
        "status": "sucesso",
        "codigo": 0,
        "mensagem": "Compra executada com sucesso",
        "preco": 125000.0,
    }

    runner = CliRunner()
    result = runner.invoke(
        compra,
        ["--symbol", "WINZ25", "--lot", "1", "--sl", "150", "--tp", "300"]
    )

    assert result.exit_code == 0
    assert "Resultado da compra" in result.output
    assert "sucesso" in result.output.lower()
    assert "125000" in result.output

