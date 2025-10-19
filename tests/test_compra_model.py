import pytest
import logging
from unittest.mock import MagicMock, patch
from mtcli_trade.models import compra_model


@pytest.fixture
def mock_mt5(mocker):
    mock = mocker.patch("mtcli_trade.models.compra_model.mt5", autospec=True)
    mock.ORDER_TYPE_BUY = 0
    mock.ORDER_TYPE_BUY_LIMIT = 2
    return mock


@pytest.fixture
def caplog_info(caplog):
    caplog.set_level(logging.INFO, logger="mtcli")
    return caplog


def test_verificar_risco_bloqueado(mocker):
    mock_ctrl = mocker.patch(
        "mtcli_trade.models.compra_model.controlar_risco", return_value=True
    )
    assert compra_model.verificar_risco() is True
    mock_ctrl.assert_called_once()


def test_verificar_risco_erro_logado(mocker, caplog_info):
    mocker.patch(
        "mtcli_trade.models.compra_model.controlar_risco", side_effect=Exception("erro")
    )
    assert compra_model.verificar_risco() is True
    assert "Erro ao verificar risco" in caplog_info.text


def test_preparar_ordem_market_sucesso(mock_mt5, mocker):
    mock_tick = MagicMock(ask=120010)
    mocker.patch("mtcli_trade.models.compra_model.inicializar", return_value=mock_tick)
    mock_criar = mocker.patch(
        "mtcli_trade.models.compra_model.criar_ordem", return_value={"symbol": "WINV25"}
    )

    ordem, is_limit = compra_model.preparar_ordem_compra("WINV25", 1.0, 100, 200, False)
    assert ordem["symbol"] == "WINV25"
    assert is_limit is False
    mock_criar.assert_called_once()


def test_preparar_ordem_limit_sucesso(mock_mt5, mocker):
    mock_tick = MagicMock()
    mocker.patch("mtcli_trade.models.compra_model.inicializar", return_value=mock_tick)
    mock_criar = mocker.patch(
        "mtcli_trade.models.compra_model.criar_ordem", return_value={"symbol": "WINV25"}
    )

    ordem, is_limit = compra_model.preparar_ordem_compra(
        "WINV25", 1.0, 100, 200, True, preco=118500
    )
    assert ordem["symbol"] == "WINV25"
    assert is_limit is True
    mock_criar.assert_called_once()


def test_preparar_ordem_sem_tick_retorna_none(mocker, caplog_info):
    mocker.patch("mtcli_trade.models.compra_model.inicializar", return_value=None)
    ordem, is_limit = compra_model.preparar_ordem_compra("WINV25", 1.0, 100, 200, False)
    assert ordem is None
    assert "Falha ao inicializar" in caplog_info.text


def test_preparar_ordem_limit_sem_preco_erro():
    with pytest.raises(ValueError, match="Preço obrigatório"):
        compra_model.preparar_ordem_compra("WINV25", 1.0, 100, 200, True)


def test_enviar_ordem_compra_sucesso(mocker):
    mock_enviar = mocker.patch(
        "mtcli_trade.models.compra_model.enviar_ordem", return_value={"retcode": 10009}
    )
    ordem = {"symbol": "WINV25"}
    resultado = compra_model.enviar_ordem_compra(ordem, False)
    assert resultado["retcode"] == 10009
    mock_enviar.assert_called_once()


def test_enviar_ordem_invalida(caplog_info):
    resultado = compra_model.enviar_ordem_compra(None, False)
    assert resultado["retcode"] is None
    assert "Ordem inválida" in caplog_info.text


def test_enviar_ordem_excecao(mocker, caplog_info):
    mocker.patch(
        "mtcli_trade.models.compra_model.enviar_ordem", side_effect=Exception("falha MT5")
    )
    resultado = compra_model.enviar_ordem_compra({"symbol": "WINV25"}, False)
    assert resultado["retcode"] is None
    assert "Erro ao enviar ordem" in caplog_info.text

