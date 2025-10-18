from mtcli.conecta import conectar, shutdown
from mtcli_trade.models.venda_model import (
    verificar_risco,
    preparar_ordem_venda,
    enviar_ordem_venda,
)
from mtcli.logger import setup_logger

log = setup_logger()


def executar_venda(
    symbol: str, lot: float, sl: float, tp: float, limit: bool, preco: float = None
):
    """Controla o fluxo completo da venda."""
    conectar()

    if verificar_risco():
        log.info("Envio de ordem bloqueado por risco diário.")
        shutdown()
        return {"status": "bloqueado", "mensagem": "Limite de prejuízo atingido."}

    try:
        ordem, is_limit = preparar_ordem_venda(symbol, lot, sl, tp, limit, preco)
        if ordem is None:
            shutdown()
            return {"status": "falha", "mensagem": "Falha ao preparar ordem."}

        resultado = enviar_ordem_venda(ordem, is_limit)
        shutdown()
        return {"status": "ok", "resultado": resultado}
    except ValueError as e:
        log.error(str(e))
        shutdown()
        return {"status": "erro", "mensagem": str(e)}
    except Exception as e:
        log.exception("Erro inesperado ao executar venda: %s", e)
        shutdown()
        return {"status": "erro", "mensagem": str(e)}
