import click


def exibir_resultado_cancelamento(resultado, ticket):
    """
    Exibe resultado do cancelamento.
    """

    if resultado is None:
        click.echo("Falha ao cancelar ordem.")
        return

    if resultado.retcode == 10009:
        click.echo(f"Ordem {ticket} cancelada com sucesso.")
    else:
        click.echo(
            f"Erro ao cancelar ordem {ticket}. "
            f"Retcode: {resultado.retcode}"
        )
