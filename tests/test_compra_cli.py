import pytest
from click.testing import CliRunner
from mtcli_trade.commands.compra import compra


def test_cli_compra_market(mock_mt5):
    runner = CliRunner()
    result = runner.invoke(compra, ["--symbol", "WINV25", "--lot", "1"])
    assert result.exit_code == 0
