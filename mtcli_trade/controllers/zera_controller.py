from ..services.positions_service import buscar_posicoes_mt5
from ..services.mt5_service import enviar_ordem_mt5
from ..models.ordem_model import criar_ordem


def zerar_posicoes(symbol=None):
    posicoes = buscar_posicoes_mt5(symbol)
    resultados = []

    for p in posicoes:
        ordem = criar_ordem_fechamento(p)
        resultados.append(enviar_ordem_mt5(ordem))

    return resultados
