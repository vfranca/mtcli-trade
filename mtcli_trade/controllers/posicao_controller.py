from mtcli_trade.models.posicao_model import Posicao

class PosicaoController:
    def __init__(self):
        self.posicao = Posicao.carregar()

    def comprar(self, qtd, preco):
        self.posicao.comprar(qtd, preco)
        return self.posicao

    def vender(self, qtd, preco):
        lucro = self.posicao.vender(qtd, preco)
        return lucro

    def status(self, preco_atual):
        return self.posicao.status(preco_atual)

    def zerar(self):
        self.posicao = Posicao.zerar()
        return self.posicao

