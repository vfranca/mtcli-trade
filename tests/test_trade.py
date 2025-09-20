import pytest
from click.testing import CliRunner
from mtcli_trade.buy import buy

def test_cli_compra_market(mock_mt5):
    runner = CliRunner()
    result = runner.invoke(buy, ["--symbol", "WINV25", "--lot", "1"])
    assert result.exit_code == 0

