import click

def exibir_resultado_venda(resultado: dict):
    """Mostra o resultado da venda no terminal."""
    status = resultado.get("status")

    if status == "bloqueado":
        click.echo("🚫 Ordem bloqueada: limite de prejuízo diário atingido.")
    elif status == "falha":
        click.echo("❌ Falha ao preparar a ordem de venda.")
    elif status == "erro":
        click.echo(f"⚠️ Erro: {resultado.get('mensagem')}")
    elif status == "ok":
        click.echo("✅ Ordem de venda enviada com sucesso.")
        click.echo(f"Detalhes: {resultado.get('resultado')}")
    else:
        click.echo("⚙️ Estado desconhecido.")
