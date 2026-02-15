import click


def exibir_resultado_fechamento(resultados, symbol):
    """
    Exibe resultado do fechamento em massa.
    """

    if not resultados:
        click.echo(f"Nenhuma posição aberta para {symbol}.")
        return

    click.echo(f"Fechamento de posições para {symbol}:")
    click.echo("------------------------------------")

    for ticket, resultado in resultados:
        if resultado and resultado.retcode == 10009:
            click.echo(f"Ticket {ticket} fechado com sucesso.")
        else:
            click.echo(
                f"Erro ao fechar ticket {ticket}. "
                f"Retcode {getattr(resultado, 'retcode', None)}."
            )
