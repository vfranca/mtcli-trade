def exibir_cancelamento(resultado, symbol=None):
    if resultado["total"] == 0:
        print(
            f"Nenhuma ordem pendente para {symbol}"
            if symbol
            else "Nenhuma ordem pendente encontrada."
        )
        return

    print(
        f"Canceladas {resultado['sucesso']} de {resultado['total']} ordens."
    )

    if resultado["falha"]:
        print(f"Falhas: {resultado['falha']}")
