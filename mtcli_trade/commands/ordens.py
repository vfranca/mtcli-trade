import click
from mtcli_trade.controllers.ordens_controller import (
    obter_ordens_pendentes,
    cancelar_ordens_pendentes,
)
from mtcli_trade.views.ordens_view import exibir_ordens, exibir_cancelar_ordens


@click.command("orders", help="Lista todas as ordens pendentes abertas, com detalhes.")
@click.version_option(package_name="mtcli-trade")
@click.option("--symbol", "-s", default=None, help="Símbolo do ativo (opcional)")
@click.option(
    "--cancelar", "-c", is_flag=True, default=False, help="Cancela todas as ordens."
)
def ordens(symbol, cancelar):
    """Lista todas as ordens pendentes (ou de um símbolo)"""
    if cancelar:
        resultados = cancelar_ordens_pedentes(symbol)
        exibir_cancelar_ordens(resultados, symbol)
        return
    ordens = obter_ordens_pendentes(symbol)
    exibir_ordens(ordens, symbol)


if __name__ == "__main__":
    ordens()
