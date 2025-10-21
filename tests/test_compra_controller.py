import logging
from unittest.mock import MagicMock

import pytest

from mtcli_trade.controllers import compra_controller


@pytest.fixture
def caplog_info(caplog):
    caplog.set_level(logging.INFO, logger="mtcli")
    return caplog


def test_executar_compra_bloqueada(mocker):
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.verificar_risco", return_value=True
    )
    resultado = compra_controller.executar_compra("WINV25", 1, 100, 200, False)
    assert resultado["status"] == "bloqueado"


def test_executar_compra_sucesso(mocker):
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.verificar_risco", return_value=False
    )
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.preparar_ordem_compra",
        return_value=(MagicMock(), False),
    )
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.enviar_ordem_compra",
        return_value={"retcode": 10009},
    )

    resultado = compra_controller.executar_compra("WINV25", 1, 100, 200, False)
    assert resultado["status"] == "ok"


def test_executar_compra_ordem_invalida(mocker):
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.verificar_risco", return_value=False
    )
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.preparar_ordem_compra",
        return_value=(None, None),
    )

    resultado = compra_controller.executar_compra("WINV25", 1, 100, 200, False)
    assert resultado["status"] == "falha"
    assert "Tick inválido" in resultado["resultado"]["mensagem"]


def test_executar_compra_mt5_recusa(mocker, caplog_info):
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.verificar_risco", return_value=False
    )
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.preparar_ordem_compra",
        return_value=(MagicMock(), False),
    )
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.enviar_ordem_compra",
        return_value={"retcode": 99999},
    )

    resultado = compra_controller.executar_compra("WINV25", 1, 100, 200, False)
    assert resultado["status"] == "falha"
    assert "MetaTrader 5 recusou" in resultado["mensagem"]
    assert "Ordem recusada" in caplog_info.text


def test_executar_compra_valueerror(mocker):
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.verificar_risco", return_value=False
    )
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.preparar_ordem_compra",
        side_effect=ValueError("Preco obrigatorio"),
    )

    resultado = compra_controller.executar_compra("WINV25", 1, 100, 200, True)
    assert resultado["status"] == "erro"
    assert "Preco obrigatorio" in resultado["mensagem"]


def test_executar_compra_excecao_generica(mocker):
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.verificar_risco", return_value=False
    )
    mocker.patch(
        "mtcli_trade.controllers.compra_controller.preparar_ordem_compra",
        side_effect=Exception("Falha inesperada"),
    )

    resultado = compra_controller.executar_compra("WINV25", 1, 100, 200, False)
    assert resultado["status"] == "erro"
    assert "Falha inesperada" in resultado["mensagem"]
