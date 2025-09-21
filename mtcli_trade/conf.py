import os

from mtcli.conf import config

SYMBOL = os.getenv("SYMBOL", config["DEFAULT"].get("symbol", fallback="WINV25"))
SL = float(os.getenv("SL", config["DEFAULT"].getfloat("sl", fallback=150)))
TP = float(os.getenv("TP", config["DEFAULT"].getfloat("tp", fallback=150)))
DIGITOS = int(os.getenv("DIGITOS", config["DEFAULT"].getint("digitos", fallback=0)))
LOSS_LIMIT = float(
    os.getenv("LOSS_LIMIT", config["DEFAULT"].getfloat("loss_limit", fallback=-180.00))
)
ARQUIVO_ESTADO = os.getenv(
    "ARQUIVO_ESTADO",
    config["DEFAULT"].get("arquivo_estado", fallback="bloqueio_risco.json"),
)
