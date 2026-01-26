"""
View responsável por exibir o resultado do envio de ordens.

Esta view:
- Não acessa MT5
- Não contém lógica de negócio
- Apenas interpreta o resultado retornado pelo controller
- Prioriza leitura por leitores de tela (NVDA / JAWS)
"""

import click


def exibir_resultado_ordem(resultado):
    """
    Exibe o resultado do envio de uma ordem.

    :param resultado: dict normalizado retornado pelo controller
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
    """
    click.echo("Ordem enviada com sucesso")
    click.echo(f"Ativo: {r.get('symbol')}")
    click.echo(f"Volume: {r.get('volume')}")
    click.echo(f"Preço: {r.get('price')}")
    click.echo(f"Ticket: {r.get('ticket')}")


def _exibir_falha(r):
    """
    Exibe mensagem de falha no envio da ordem.
    """
    click.echo("Falha ao enviar ordem")
    click.echo(f"Código de retorno: {r.get('retcode')}")
    if r.get("mensagem"):
        click.echo(f"Mensagem: {r.get('mensagem')}")
