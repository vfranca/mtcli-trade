import pytest
from unittest.mock import patch, MagicMock
from mtcli_trade.models.posicoes_model import (
    buscar_posicoes,
    editar_posicao,
    encerra_posicoes,
)


@pytest.fixture
def mock_mt5(mocker):
    mock_mt5 = mocker.patch("mtcli_trade.models.posicoes_model.mt5", autospec=True)
    return mock_mt5


@pytest.fixture
def mock_conexao(mocker):
    return mocker.patch("mtcli_trade.models.posicoes_model.mt5_conexao", autospec=True)


def test_buscar_posicoes(mock_mt5, mock_conexao):
    mock_mt5.positions_get.return_value = [MagicMock(symbol="WINV25")]
    resultado = buscar_posicoes()
    assert len(resultado) == 1
    mock_mt5.positions_get.assert_called_once()


def test_editar_posicao_sucesso(mock_mt5, mock_conexao):
    mock_pos = MagicMock(sl=100, tp=200, symbol="WINV25", magic=1)
    mock_mt5.positions_get.return_value = [mock_pos]
    mock_mt5.order_send.return_value = MagicMock(retcode=mt5.TRADE_RETCODE_DONE)

    resultado = editar_posicao(ticket=1, novo_sl=110, novo_tp=210)
    assert resultado.retcode == mt5.TRADE_RETCODE_DONE


def test_editar_posicao_inexistente(mock_mt5, mock_conexao, caplog):
    mock_mt5.positions_get.return_value = None
    with pytest.raises(ValueError):
        editar_posicao(999)
    assert "Posição com ticket 999 não encontrada" in caplog.text


def test_editar_posicao_falha_envio(mock_mt5, mock_conexao, caplog):
    mock_pos = MagicMock(sl=100, tp=200, symbol="WINV25", magic=1)
    mock_mt5.positions_get.return_value = [mock_pos]
    mock_mt5.order_send.return_value = None

    with pytest.raises(RuntimeError):
        editar_posicao(ticket=1, novo_sl=120, novo_tp=220)
    assert "order_send retornou None" in caplog.text


def test_editar_posicao_retcode_invalido(mock_mt5, mock_conexao, caplog):
    mock_pos = MagicMock(sl=100, tp=200, symbol="WINV25", magic=1)
    mock_mt5.positions_get.return_value = [mock_pos]
    mock_mt5.order_send.return_value = MagicMock(retcode=123)

    with pytest.raises(RuntimeError):
        editar_posicao(ticket=1, novo_sl=120, novo_tp=220)
    assert "Falha ao editar posição" in caplog.text


def test_encerra_posicoes(mock_mt5, mock_conexao, caplog):
    mock_pos = MagicMock(
        symbol="WINV25", type=mt5.POSITION_TYPE_BUY, volume=1.0, ticket=123, magic=1
    )
    mock_tick = MagicMock(bid=120000, ask=120010)
    mock_mt5.positions_get.return_value = [mock_pos]
    mock_mt5.symbol_info_tick.return_value = mock_tick
    mock_mt5.order_send.return_value = MagicMock(retcode=mt5.TRADE_RETCODE_DONE)

    resultados = encerra_posicoes()
    assert len(resultados) == 1
    assert "encerrada com sucesso" in caplog.text


def test_encerra_posicoes_sem_tick(mock_mt5, mock_conexao, caplog):
    mock_pos = MagicMock(
        symbol="WINV25", type=mt5.POSITION_TYPE_BUY, volume=1.0, ticket=123, magic=1
    )
    mock_mt5.positions_get.return_value = [mock_pos]
    mock_mt5.symbol_info_tick.return_value = None

    resultados = encerra_posicoes()
    assert resultados == []
    assert "Não foi possível recuperar ticks" in caplog.text


def test_encerra_posicoes_falha_envio(mock_mt5, mock_conexao, caplog):
    mock_pos = MagicMock(
        symbol="WINV25", type=mt5.POSITION_TYPE_BUY, volume=1.0, ticket=123, magic=1
    )
    mock_tick = MagicMock(bid=120000, ask=120010)
    mock_mt5.positions_get.return_value = [mock_pos]
    mock_mt5.symbol_info_tick.return_value = mock_tick
    mock_mt5.order_send.return_value = None

    resultados = encerra_posicoes()
    assert resultados[0] is None
    assert "order_send retornou None" in caplog.text


def test_encerra_posicoes_lista_vazia(mock_mt5, mock_conexao, caplog):
    mock_mt5.positions_get.return_value = []
    resultados = encerra_posicoes()
    assert resultados == []
    assert "Nenhuma posição aberta" in caplog.text


def test_mt5_conexao_excecao(mock_mt5, mocker, caplog):
    mock_context = mocker.patch("posicoes_model.mt5_conexao")
    mock_context.side_effect = ConnectionError("Falha de conexão MT5")

    with pytest.raises(ConnectionError):
        buscar_posicoes()
    assert "Falha de conexão MT5" in caplog.text
