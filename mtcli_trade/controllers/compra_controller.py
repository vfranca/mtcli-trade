from mtcli.logger import setup_logger
from mtcli_trade.models.compra_model import verificar_risco, enviar_compra

log = setup_logger()


def _formatar_retorno(res, etapa: str):
    """Formata e registra o resultado de cada etapa do processo de compra."""
    log.info(f"{etapa}: status={res['status']} código={res['codigo']} mensagem={res['mensagem']} preço={res['preco']}")
    return res


def processar_compra(symbol, lot, sl, tp, limit, preco):
    """Processa uma ordem de compra com verificação de risco e envio seguro."""
    try:
        # Etapa 1: Verificação de risco
        if (res := verificar_risco()):
            return _formatar_retorno(res, "Verificação de risco")

        # Etapa 2: Envio da compra
        res = enviar_compra(symbol, lot, sl, tp, limit, preco)
        return _formatar_retorno(res, "Envio da compra")

    except Exception as e:
        log.exception(f"Erro ao processar compra para {symbol}: {e}")
        return {
            "status": "erro",
            "codigo": -1,
            "mensagem": f"Erro inesperado ao processar compra: {e}",
            "preco": preco,
        }
