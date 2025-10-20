import click
from mtcli_trade.controllers.venda_controller import executar_venda
from mtcli_trade.views.ordem_view import exibir_resultado_ordem
from mtcli_trade.conf import SYMBOL, LOT, SL, TP


@click.command(
    "venda", help="Envia ordem de compra (market ou limit) com SL e TP opcionais."
)
@click.version_option(package_name="mtcli-trade")
@click.option(
    "--symbol", "-s", default=SYMBOL, help="Símbolo do ativo (default WINV25)."
)
@click.option(
    "--lot", type=float, default=LOT, help="Quantidade de contratos (default=1.0)"
)
@click.option("--sl", type=float, default=SL, help="Stop loss (em pontos).")
@click.option("--tp", type=float, default=TP, help="Take profit (em pontos).")
@click.option("--limit", "-l", is_flag=True, help="Envia ordem pendente (buy limit).")
@click.option("--preco", "-pr", type=float, default=None, help="Preço da ordem limit.")
def venda_cmd(symbol, lot, sl, tp, limit, preco):
    """Executa o fluxo completo de compra."""
    resultado = executar_venda(symbol, lot, sl, tp, limit, preco)
    exibir_resultado_ordem(resultado)


if __name__ == "__main__":
    venda_cmd()
