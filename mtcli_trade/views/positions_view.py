"""
View responsável pela exibição de posições abertas no terminal.

Esta view:
- Não acessa MT5
- Não contém lógica de negócio
- Apenas apresenta dados já normalizados
- Prioriza leitura por leitores de tela (NVDA, JAWS)
"""

import click


# ---------------------------------------------------------
# Função principal de exibição
# ---------------------------------------------------------

def exibir_posicoes(posicoes, symbol=None):
    """
    Exibe posições abertas no terminal.

    :param posicoes: lista de dicionários normalizados
    :param symbol: ativo filtrado (opcional)
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


# ---------------------------------------------------------
# Exibição individual (formato acessível)
# ---------------------------------------------------------

def _exibir_posicao(p):
    """
    Exibe uma única posição em formato linear otimizado
    para leitura por leitores de tela.
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
