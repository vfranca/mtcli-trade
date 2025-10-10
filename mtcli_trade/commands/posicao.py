import click
from mtcli_trade.controllers.posicao_controller import PosicaoController
from mtcli_trade.views.posicao_view import mostrar_status

@click.group()
def posicao():
    """Gerencia posição simulada com preço médio e lucro."""
    pass

@posicao.command()
@click.argument("qtd", type=int)
@click.argument("preco", type=float)
def comprar(qtd, preco):
    """Adiciona contratos à posição."""
    ctrl = PosicaoController()
    pos = ctrl.comprar(qtd, preco)
click.echo(f"📈 Comprado qtd a preco. Novo preço médio: pos.preco_medio:.2f")

@posicao.command()
@click.argument("qtd", type=int)
@click.argument("preco", type=float)
def vender(qtd, preco):
    """Remove contratos da posição."""
    ctrl = PosicaoController()
    try:
        lucro = ctrl.vender(qtd, preco)
        click.echo(f"📉 Vendido qtd a preco. Lucro parcial: R{lucro:.2f}")
    except ValueError as e:
        click.echo(f"❌ {e}")

@posicao.command()
@click.argument("preco_atual", type=float)
def status(preco_atual):
    """Mostra status da posição no preço atual."""
    ctrl = PosicaoController()
    mostrar_status(ctrl.status(preco_atual))

@posicao.command()
def zerar():
    """Zera a posição e limpa o histórico."""
    ctrl = PosicaoController()
    ctrl.zerar()
    click.echo("🔄 Posição zerada e dados limpos.")

