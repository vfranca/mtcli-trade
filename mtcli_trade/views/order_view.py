"""
View responsável por exibir resultados de ordens no terminal.

Características:
- Não contém regras de negócio
- Não acessa MetaTrader 5
- Recebe apenas dados normalizados do controller
- Saída otimizada para leitores de tela (NVDA / JAWS)
- Estrutura linear, sem elementos visuais complexos
"""

import click


def exibir_resultado_ordem(resultado):
    """
    Exibe o resultado do envio de uma ordem.

    Args:
        resultado (dict): Dicionário normalizado retornado pelo controller.

    Estrutura esperada:
        {
            "sucesso": bool,
            "retcode": int,
            "mensagem": str,
            "ticket": int | None,
            "symbol": str,
            "volume": float,
            "price": float
        }
    """
    if not resultado:
        click.echo("Nenhum resultado retornado da ordem.")
        return

    if resultado.get("sucesso"):
        _exibir_sucesso(resultado)
    else:
        _exibir_falha(resultado)


# ----------------------------------------------------------------------


def _exibir_sucesso(r):
    """
    Exibe mensagem de sucesso no envio da ordem.

    Mantém saída simples e sequencial para facilitar leitura
    por leitores de tela.
    """
    click.echo("Ordem enviada com sucesso.")
    click.echo(f"Ativo: {r.get('symbol')}")
    click.echo(f"Volume: {r.get('volume')}")
    click.echo(f"Preço executado: {r.get('price')}")
    click.echo(f"Ticket: {r.get('ticket')}")
    click.echo("Status: CONFIRMADO.")


def _exibir_falha(r):
    """
    Exibe mensagem de falha no envio da ordem.
    """
    click.echo("Falha ao enviar ordem.")
    click.echo(f"Código de retorno: {r.get('retcode')}")

    mensagem = r.get("mensagem")
    if mensagem:
        click.echo(f"Mensagem do servidor: {mensagem}")

    click.echo("Status: REJEITADO.")
