"""
Serviço para rodar monitor como daemon (Unix).
No Windows o comportamento será normal.
"""

import os
import sys


def daemonizar():
    """
    Executa processo como daemon (Linux/macOS).
    """

    if os.name == "nt":
        # Windows não suporta fork
        return

    if os.fork() > 0:
        sys.exit()

    os.setsid()

    if os.fork() > 0:
        sys.exit()

    sys.stdout.flush()
    sys.stderr.flush()
