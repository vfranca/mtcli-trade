"""
View responsável pela exibição de posições abertas no terminal.

- Não acessa MT5
- Não contém lógica de negócio
- Prioriza leitura por screen readers
"""

import click


def exibir_posicoes(posicoes, symbol=None):
    """
    Exibe posições abertas no terminal.
    """

    if not posicoes:
        click.echo(
            f"Nenhuma posição aberta para {symbol}."
            if symbol
            else "Nenhuma posição aberta."
        )
        return

    header = (
        f"Posições abertas para {symbol}:"
        if symbol
        else "Posições abertas:"
    )

    click.echo(header)
    click.echo("-" * len(header))

    for posicao in posicoes:
        _exibir_posicao(posicao)


def _exibir_posicao(p):
    """
    Exibição individual otimizada para leitores de tela.
    """

    click.echo(
        f"Ticket {p['ticket']}. "
        f"Tipo {p['tipo']}. "
        f"Ativo {p['symbol']}. "
        f"Volume {p['volume']}. "
        f"Preço de abertura {p['preco_abertura']}. "
        f"Lucro atual {p['lucro']}. "
        f"Swap {p['swap']}."
    )


# ---------------------------------------------------------
# NOVO: Resumo consolidado
# ---------------------------------------------------------

def exibir_resumo(resumo: dict):
    """
    Exibe resumo consolidado das posições.
    """

    click.echo("\nResumo consolidado:")
    click.echo("--------------------")

    click.echo(f"Total de posições: {resumo['total_posicoes']}.")
    click.echo(f"Volume total: {resumo['volume_total']}.")
    click.echo(f"Lucro total: {resumo['lucro_total']}.")
    click.echo(f"Swap total: {resumo['swap_total']}.")
