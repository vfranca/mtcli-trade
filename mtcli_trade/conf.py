"""
Configurações padrão do plugin mtcli-trade.

Prioridade:
1. Variáveis de ambiente
2. Seção [trade] no mtcli.ini
3. Fallback interno
"""

import os
from mtcli.conf import config

SECTION = "TRADE"


def _get_optional_float(env_key, config_key):
    value = os.getenv(env_key)

    if value is not None:
        return float(value)

    if config.has_option(SECTION, config_key):
        return config.getfloat(SECTION, config_key)

    return None


SYMBOL = os.getenv("SYMBOL", config[SECTION].get("symbol", fallback="WINV25"))
LOT = float(os.getenv("LOT", config[SECTION].getfloat("lot", fallback=1.0)))

SL = _get_optional_float("SL", "sl")
TP = _get_optional_float("TP", "tp")

DIGITOS = int(os.getenv("DIGITOS", config[SECTION].getint("digitos", fallback=0)))

LOSS_LIMIT = float(
    os.getenv("LOSS_LIMIT", config[SECTION].getfloat("loss_limit", fallback=-180.0))
)

STATUS_FILE = os.getenv(
    "STATUS_FILE",
    config[SECTION].get("status_file", fallback="bloqueio.json"),
)
