import logging
from unittest.mock import MagicMock

import pytest

from mtcli_trade.models.posicoes_model import (
    buscar_posicoes,
    editar_posicao,
    encerra_posicoes,
)


@pytest.fixture
def mock_mt5(mocker):
    """Mocka o módulo MetaTrader5 dentro de todos os models usados."""
    mock_mt5 = mocker.Mock()
    mock_mt5.TRADE_RETCODE_DONE = 10009
    mock_mt5.TRADE_RETCODE_PLACED = 10008
    mock_mt5.POSITION_TYPE_BUY = 0
    mock_mt5.POSITION_TYPE_SELL = 1
    mock_mt5.ORDER_TYPE_SELL = 1
    mock_mt5.ORDER_TYPE_BUY = 0
    mock_mt5.TRADE_ACTION_SLTP = 2
    mock_mt5.order_send.return_value = MagicMock(retcode=10009)

    # ✅ Adiciona retorno realista para symbol_info
    mock_symbol_info = MagicMock(point=0.01)
    mock_mt5.symbol_info.return_value = mock_symbol_info

    # ✅ Patches aplicados a todos os módulos que utilizam mt5
    mocker.patch("mtcli_trade.models.posicoes_model.mt5", mock_mt5)
    mocker.patch("mtcli_trade.models.ordem_model.mt5", mock_mt5)
    return mock_mt5


@pytest.fixture
def mock_conexao(mocker):
    """Mocka o contexto mt5_conexao para evitar conexões reais."""
    return mocker.patch("mtcli_trade.models.posicoes_model.mt5_conexao", autospec=True)


# ------------------------
# TESTES DE BUSCA
# ------------------------


def test_buscar_posicoes(mock_mt5, mock_conexao):
    mock_mt5.positions_get.return_value = [MagicMock(symbol="WINV25")]
    resultado = buscar_posicoes()
    assert len(resultado) == 1
    mock_mt5.positions_get.assert_called_once()


# ------------------------
# TESTES DE EDIÇÃO
# ------------------------


def test_editar_posicao_sucesso(mock_mt5, mock_conexao, caplog):
    mock_pos = MagicMock(ticket=1, sl=100, tp=200, symbol="WINV25", magic=1)
    mock_mt5.positions_get.return_value = [mock_pos]
    mock_mt5.order_send.return_value = MagicMock(retcode=10009)

    caplog.set_level(logging.INFO, logger="mtcli")
    resultado = editar_posicao(ticket=1, sl=110, tp=210)

    assert resultado is True
    assert any("editada com sucesso" in msg for msg in caplog.messages)


def test_editar_posicao_inexistente(mock_mt5, mock_conexao, caplog):
    mock_mt5.positions_get.return_value = []
    caplog.set_level(logging.WARNING, logger="mtcli")
    resultado = editar_posicao(ticket=999)
    assert resultado is False
    # Verificação flexível e tolerante à acentuação
    assert "nenhuma posição encontrada" in caplog.text.lower()


def test_editar_posicao_falha_envio(mock_mt5, mock_conexao, caplog):
    mock_pos = MagicMock(ticket=1, sl=100, tp=200, symbol="WINV25")
    mock_mt5.positions_get.return_value = [mock_pos]
    mock_mt5.order_send.return_value = MagicMock(retcode=99999)

    caplog.set_level(logging.ERROR, logger="mtcli")
    resultado = editar_posicao(ticket=1, sl=120, tp=220)

    assert resultado is False
    assert "falha ao editar" in caplog.text.lower()


# ------------------------
# TESTES DE ENCERRAMENTO
# ------------------------


def test_encerra_posicoes_sucesso(mock_mt5, mock_conexao, caplog):
    mock_pos = MagicMock(
        symbol="WINV25", type=mock_mt5.POSITION_TYPE_BUY, volume=1.0, ticket=123
    )
    mock_tick = MagicMock(bid=120000, ask=120010)
    mock_mt5.positions_get.return_value = [mock_pos]
    mock_mt5.symbol_info_tick.return_value = mock_tick
    mock_mt5.order_send.return_value = MagicMock(retcode=10009)

    caplog.set_level(logging.INFO, logger="mtcli")
    resultados = encerra_posicoes()

    assert len(resultados) == 1
    assert any("encerrada com sucesso" in msg for msg in caplog.messages)


def test_encerra_posicoes_sem_tick(mock_mt5, mock_conexao, caplog):
    mock_pos = MagicMock(symbol="WINV25", type=mock_mt5.POSITION_TYPE_BUY, volume=1.0)
    mock_mt5.positions_get.return_value = [mock_pos]
    mock_mt5.symbol_info_tick.return_value = None

    resultados = encerra_posicoes()
    assert resultados == []
    assert "falha ao obter tick" in caplog.text.lower()


def test_encerra_posicoes_falha_envio(mock_mt5, mock_conexao, caplog):
    mock_pos = MagicMock(symbol="WINV25", type=mock_mt5.POSITION_TYPE_BUY, volume=1.0)
    mock_tick = MagicMock(bid=120000, ask=120010)
    mock_mt5.positions_get.return_value = [mock_pos]
    mock_mt5.symbol_info_tick.return_value = mock_tick
    mock_mt5.order_send.return_value = MagicMock(retcode=99999)

    caplog.set_level(logging.INFO, logger="mtcli")
    resultados = encerra_posicoes()
    assert len(resultados) == 1
    assert "falha ao encerrar" in caplog.text.lower()


def test_encerra_posicoes_lista_vazia(mock_mt5, mock_conexao, caplog):
    mock_mt5.positions_get.return_value = []
    caplog.set_level(logging.INFO, logger="mtcli")
    resultados = encerra_posicoes()
    assert resultados == []
    assert "nenhuma posição aberta" in caplog.text.lower()


def test_mt5_conexao_excecao(mocker, caplog):
    mock_context = mocker.patch("mtcli_trade.models.posicoes_model.mt5_conexao")
    mock_context.side_effect = ConnectionError("Falha de conexão MT5")

    caplog.set_level(logging.ERROR, logger="mtcli")
    with pytest.raises(ConnectionError):
        buscar_posicoes()
