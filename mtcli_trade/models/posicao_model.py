import json
from pathlib import Path

ARQUIVO_ESTADO = Path.home() / ".mtcli_posicao.json"

class Posicao:
    def __init__(self, contratos=0, preco_medio=0.0, lucro_realizado=0.0):
        self.contratos = contratos
        self.preco_medio = preco_medio
        self.lucro_realizado = lucro_realizado

    def comprar(self, qtd, preco):
        if self.contratos == 0:
            self.preco_medio = preco
        else:
            total_custo = self.preco_medio * self.contratos + preco * qtd
            self.preco_medio = total_custo / (self.contratos + qtd)
        self.contratos += qtd
        self.salvar()

    def vender(self, qtd, preco):
        if qtd > self.contratos:
            raise ValueError("Contratos insuficientes")

        lucro = (preco - self.preco_medio) * qtd * 0.2
        self.lucro_realizado += lucro
        self.contratos -= qtd
        if self.contratos == 0:
            self.preco_medio = 0.0
        self.salvar()
        return lucro

    def status(self, preco_atual):
        lucro_aberto = (preco_atual - self.preco_medio) * self.contratos * 0.2
        return {
            "contratos": self.contratos,
            "preco_medio": self.preco_medio,
            "lucro_aberto": lucro_aberto,
            "lucro_realizado": self.lucro_realizado,
            "lucro_total": lucro_aberto + self.lucro_realizado,
        }

    def salvar(self):
        with open(ARQUIVO_ESTADO, "w") as f:
            json.dump(self.dict, f)

    @classmethod
    def carregar(cls):
        if ARQUIVO_ESTADO.exists():
            with open(ARQUIVO_ESTADO) as f:
                dados = json.load(f)
                return cls(**dados)
        return cls()

    @classmethod
    def zerar(cls):
        ARQUIVO_ESTADO.unlink(missing_ok=True)
        return cls()

