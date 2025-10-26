import click


def exibir_compra(resultado):
    """Exibe o resultado da compra de forma acessível no terminal."""
    click.echo("Resultado da compra:")
    click.echo(f"  Status:   {resultado['status']}")
    click.echo(f"  Código:   {resultado['codigo']}")
    click.echo(f"  Mensagem: {resultado['mensagem']}")
    click.echo(f"  Preço:    {resultado['preco']:.2f}")
