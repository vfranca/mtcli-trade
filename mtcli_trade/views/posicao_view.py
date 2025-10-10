import click

def mostrar_status(status):
    click.echo(f"\n📊 CONTRATOS: {status['contratos']}")
    click.echo(f"🎯 PREÇO MÉDIO: {status['preco_medio']:.2f}")
    click.echo(f"💰 LUCRO ABERTO: Rstatus['lucro_aberto']:.2f")
    click.echo(f"✅ LUCRO REALIZADO: R{status['lucro_realizado']:.2f}")
    click.echo(f"🔢 TOTAL: R${status['lucro_total']:.2f}\n")

