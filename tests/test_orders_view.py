from mtcli_trade.views.orders_view import exibir_ordens
from click.testing import CliRunner


def test_exibir_ordens_vazias():
    runner = CliRunner()
    result = runner.invoke(lambda: exibir_ordens([], symbol="WIN"))
    assert "Nenhuma ordem" in result.output


def test_exibir_ordens_ok():
    runner = CliRunner()
    ordens = [
        {"tipo": "COMPRA", "symbol": "WIN", "volume": 1, "preco": 120.5, "ticket": 111}
    ]
    result = runner.invoke(lambda: exibir_ordens(ordens))
    assert "COMPRA WIN" in result.output
