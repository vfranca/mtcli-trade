"""
Risk Engine centralizado com persistência em JSON.
Responsável por controle de stop diário.
"""

import json
import os
from datetime import date


class RiskEngine:

    def __init__(self, arquivo: str = "risk_state.json"):
        self.arquivo = arquivo
        self.estado = self._carregar_estado()

    def _carregar_estado(self):

        if not os.path.exists(self.arquivo):
            return {"data": str(date.today()), "lucro": 0.0}

        with open(self.arquivo, "r") as f:
            return json.load(f)

    def atualizar_lucro(self, lucro_atual: float):

        hoje = str(date.today())

        if self.estado["data"] != hoje:
            self.estado = {"data": hoje, "lucro": 0.0}

        self.estado["lucro"] = lucro_atual
        self._salvar()

    def atingiu_stop(self, limite: float) -> bool:

        return self.estado["lucro"] <= -abs(limite)

    def _salvar(self):

        with open(self.arquivo, "w") as f:
            json.dump(self.estado, f)
