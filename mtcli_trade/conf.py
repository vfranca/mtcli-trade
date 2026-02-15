"""
Configurações padrão do plugin mtcli-trade.

Prioridade:
1. Variáveis de ambiente
2. Seção [trade] no mtcli.ini
3. Fallback interno

Todas as variáveis são convertidas para tipos seguros.
"""

import os
from mtcli.conf import config

SECTION = "TRADE"

SYMBOL = os.getenv("SYMBOL", config[SECTION].get("symbol", fallback="WINV25"))
LOT = float(os.getenv("LOT", config[SECTION].getfloat("lot", fallback=1.0)))
SL = float(os.getenv("SL", config[SECTION].getfloat("sl", fallback=150)))
TP = float(os.getenv("TP", config[SECTION].getfloat("tp", fallback=150)))
DIGITOS = int(os.getenv("DIGITOS", config[SECTION].getint("digitos", fallback=0)))
LOSS_LIMIT = float(
    os.getenv("LOSS_LIMIT", config[SECTION].getfloat("loss_limit", fallback=-180.0))
)
STATUS_FILE = os.getenv(
    "STATUS_FILE",
    config[SECTION].get("status_file", fallback="bloqueio.json"),
)
