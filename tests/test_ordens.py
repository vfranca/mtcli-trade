import time
from unittest.mock import MagicMock, patch

from click.testing import CliRunner
import pytest

from mtcli_trade.commands.ordens_cli import ordens_cmd
from mtcli_trade.controllers.ordens_controller import (
    cancelar_ordens_pendentes,
    obter_ordens_pendentes,
)
from mtcli_trade.views.ordens_view import exibir_cancelar_ordens, exibir_ordens


# ==== UNIT TESTS - MODEL ====
@pytest.fixture
def mock_mt5(mocker):
    mt5_mock = mocker.patch("mtcli_trade.models.ordens_model.mt5")
    mt5_mock.orders_get.return_value = [
        MagicMock(
            ticket=123, symbol="WINV25", type=2, volume_current=1.0, price_open=150000
        )
    ]
    mt5_mock.ORDER_TYPE_BUY_LIMIT = 2
    mt5_mock.ORDER_TYPE_SELL_LIMIT = 3
    mt5_mock.TRADE_ACTION_REMOVE = 1
    mt5_mock.TRADE_RETCODE_DONE = 10009
    mt5_mock.order_send.return_value = MagicMock(retcode=10009)
    return mt5_mock


def test_buscar_ordens(mock_mt5):
    from mtcli_trade.models.ordens_model import buscar_ordens

    result = buscar_ordens("WINV25")
    assert isinstance(result, list)
    assert result[0].symbol == "WINV25"


def test_formatar_ordem(mock_mt5):
    from mtcli_trade.models.ordens_model import formatar_ordem

    ordem = MagicMock(
        symbol="WINV25", type=2, volume_current=1.0, price_open=150000, ticket=123
    )
    fmt = formatar_ordem(ordem)
    assert fmt["symbol"] == "WINV25"
    assert "preco" in fmt


def test_cancelar_ordens(mock_mt5):
    from mtcli_trade.models.ordens_model import cancelar_ordens

    result = cancelar_ordens("WINV25")
    assert isinstance(result, list)
    assert result[0].retcode == 10009


def test_cancelar_ordens_vazio(mocker):
    mocker.patch("mtcli_trade.models.ordens_model.mt5.orders_get", return_value=None)
    from mtcli_trade.models.ordens_model import cancelar_ordens

    result = cancelar_ordens()
    assert result == []


# ==== UNIT TESTS - CONTROLLER ====
@pytest.fixture
def mock_ordens_model(mocker):
    mocker.patch(
        "mtcli_trade.models.ordens_model.buscar_ordens",
        return_value=[MagicMock(ticket=1)],
    )
    mocker.patch(
        "mtcli_trade.models.ordens_model.formatar_ordem", return_value={"ticket": 123}
    )
    mocker.patch(
        "mtcli_trade.models.ordens_model.cancelar_ordens",
        return_value=[{"retcode": 10009}],
    )
    return mocker


def test_obter_ordens_pendentes(mock_ordens_model):
    result = obter_ordens_pendentes()
    assert isinstance(result, list)
    assert result[0]["ticket"] == 123


def test_cancelar_ordens_pendentes(mocker):
    mocker.patch(
        "mtcli_trade.controllers.ordens_controller.cancelar_ordens",
        return_value=[{"retcode": 10009}],
    )

    result = cancelar_ordens_pendentes()
    assert isinstance(result, list)
    assert result[0]["retcode"] == 10009


# ==== UNIT TESTS - VIEW ====
@pytest.mark.parametrize(
    "ordens, esperado",
    [
        (
            [
                {
                    "symbol": "WINV25",
                    "preco": 150000,
                    "volume": 1,
                    "ticket": 123,
                    "tipo": "COMPRA",
                }
            ],
            "WINV25",
        ),
        ([], "nenhuma ordem"),
    ],
)
def test_exibir_ordens(ordens, esperado, capsys):
    exibir_ordens(ordens)
    captured = capsys.readouterr()
    assert esperado.lower() in captured.out.lower()


@pytest.mark.parametrize(
    "resultados, esperado",
    [
        ([MagicMock(retcode=10009, order=123)], "cancelada"),
        ([MagicMock(retcode=0, order=321)], "falha"),
        ([], "nenhuma ordem"),
    ],
)
def test_exibir_cancelar_ordens(resultados, esperado, capsys):
    exibir_cancelar_ordens(resultados, "WINV25")
    captured = capsys.readouterr()
    assert esperado.lower() in captured.out.lower()


# ==== INTEGRATION TESTS - CLI + PERFORMANCE ====
@pytest.fixture
def runner():
    return CliRunner()


def test_cli_ordens_lista(runner):
    with patch(
        "mtcli_trade.controllers.ordens_controller.obter_ordens_pendentes"
    ) as mock_exec:
        mock_exec.return_value = [
            {"symbol": "WINV25", "preco": 150000, "ticket": 123, "tipo": "COMPRA"}
        ]
        start = time.perf_counter()
        result = runner.invoke(ordens_cmd, [])
        duration = time.perf_counter() - start
        assert result.exit_code == 0
        assert "winv25" in result.output.lower()
        assert duration < 0.5


def test_cli_ordens_cancelar(runner):
    with patch(
        "mtcli_trade.controllers.ordens_controller.cancelar_ordens_pendentes"
    ) as mock_cancel:
        mock_cancel.return_value = [{"retcode": 10009, "order": 123}]
        start = time.perf_counter()
        result = runner.invoke(ordens_cmd, ["--cancelar"])
        duration = time.perf_counter() - start
        assert "cancelada" in result.output.lower()
        assert duration < 0.5


def test_cli_ordens_filtrar_symbol(runner):
    with patch(
        "mtcli_trade.commands.ordens_cli.obter_ordens_pendentes",
        return_value=[
            {
                "symbol": "WDOX25",
                "preco": 5100,
                "volume": 1,
                "ticket": 999,
                "tipo": "COMPRA",
            }
        ],
    ):
        start = time.perf_counter()
        result = runner.invoke(ordens_cmd, ["--symbol", "WDOX25"])
        duration = time.perf_counter() - start
        assert "wdox25" in result.output.lower()
        assert duration < 0.5
