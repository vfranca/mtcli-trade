import pytest
from unittest.mock import patch, MagicMock

from mtcli_trade.controllers import compra_controller
from mtcli_trade.models import compra_model
from mtcli_trade.views import compra_view


# ============================================================
# 🧩 Cenário 1 — Integração: compra a mercado bem-sucedida
# ============================================================

@patch("mtcli_trade.models.compra_model.mt5")
@patch("mtcli_trade.models.compra_model.controlar_risco", return_value=False)
def test_fluxo_integrado_sucesso(mock_risco, mock_mt5, capsys):
    """Fluxo completo de compra a mercado bem-sucedida, com mocks do MT5."""

    # --- Simulação de resposta de tick e ordem ---
    mock_tick = MagicMock()
    mock_tick.ask = 125000.0
    mock_mt5.symbol_info_tick.return_value = mock_tick
    mock_mt5.symbol_select.return_value = True

    resultado_mt5 = MagicMock()
    resultado_mt5.retcode = mock_mt5.TRADE_RETCODE_DONE
    resultado_mt5.comment = "Ordem executada"
    resultado_mt5.price = 125000.0
    mock_mt5.order_send.return_value = resultado_mt5
    mock_mt5.TRADE_RETCODE_DONE = 0
    mock_mt5.TRADE_RETCODE_PLACED = 10009

    # --- Executa o fluxo completo ---
    res = compra_controller.processar_compra(
        symbol="WINZ25", lot=1.0, sl=150, tp=300, limit=False, preco=None
    )

    # --- Exibe via view ---
    compra_view.exibir_compra(res)
    saida = capsys.readouterr().out

    # --- Validações ---
    assert res["status"] == "sucesso"
    assert "Ordem executada" in res["mensagem"]
    assert "125000" in saida
    assert "Resultado da compra" in saida


# ============================================================
# 🚫 Cenário 2 — Integração: bloqueio de risco diário
# ============================================================

@patch("mtcli_trade.models.compra_model.mt5")
@patch("mtcli_trade.models.compra_model.controlar_risco", return_value=True)
def test_fluxo_integrado_bloqueio_risco(mock_risco, mock_mt5, capsys):
    """Fluxo completo onde o risco bloqueia a operação."""

    res = compra_controller.processar_compra(
        symbol="WINZ25", lot=1.0, sl=150, tp=300, limit=False, preco=None
    )

    compra_view.exibir_compra(res)
    saida = capsys.readouterr().out

    assert res["status"] == "bloqueado"
    assert "prejuízo" in res["mensagem"].lower()
    assert "bloqueado" in saida


# ============================================================
# ⚠️ Cenário 3 — Integração: erro de preço ausente em ordem pendente
# ============================================================

@patch("mtcli_trade.models.compra_model.mt5")
@patch("mtcli_trade.models.compra_model.controlar_risco", return_value=False)
def test_fluxo_integrado_preco_pendente(mock_risco, mock_mt5, capsys):
    """Fluxo completo simulando erro de preço não informado para ordem limit."""

    mock_tick = MagicMock()
    mock_tick.ask = 125000.0
    mock_mt5.symbol_info_tick.return_value = mock_tick
    mock_mt5.symbol_select.return_value = True

    res = compra_controller.processar_compra(
        symbol="WINZ25", lot=1.0, sl=150, tp=300, limit=True, preco=None
    )

    compra_view.exibir_compra(res)
    saida = capsys.readouterr().out

    assert res["status"] == "falha"
    assert "preco" in res["mensagem"].lower()
    assert "falha" in saida.lower()


# ============================================================
# 💣 Cenário 4 — Integração: falha inesperada no envio
# ============================================================

@patch("mtcli_trade.models.compra_model.mt5")
@patch("mtcli_trade.models.compra_model.controlar_risco", return_value=False)
def test_fluxo_integrado_falha_envio(mock_risco, mock_mt5, capsys):
    """Fluxo completo simulando erro no envio da ordem."""

    mock_tick = MagicMock()
    mock_tick.ask = 125000.0
    mock_mt5.symbol_info_tick.return_value = mock_tick
    mock_mt5.symbol_select.return_value = True
    mock_mt5.order_send.side_effect = Exception("Falha no envio MT5")

    res = compra_controller.processar_compra(
        symbol="WINZ25", lot=1.0, sl=150, tp=300, limit=False, preco=None
    )

    compra_view.exibir_compra(res)
    saida = capsys.readouterr().out

    assert res["status"] == "erro"
    assert "falha" in res["mensagem"].lower() or "erro" in res["mensagem"].lower()
    assert "erro" in saida.lower()
