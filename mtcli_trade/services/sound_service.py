"""
Serviço de alerta sonoro para eventos de trading.

Eventos suportados:
- nova posição aberta
- posição fechada

Compatível com Windows.
"""

import sys


class SoundService:
    """
    Serviço responsável por emitir sinais sonoros.

    Em Windows utiliza winsound.
    Em outros sistemas apenas ignora silenciosamente.
    """

    @staticmethod
    def _beep(freq: int, duration: int) -> None:
        """
        Executa beep no Windows.

        :param freq: Frequência do som em Hz.
        :param duration: Duração em milissegundos.
        """
        if sys.platform.startswith("win"):
            try:
                import winsound
                winsound.Beep(freq, duration)
            except Exception:
                pass  # Falha silenciosa
        else:
            pass  # Outros sistemas ignoram

    @classmethod
    def nova_posicao(cls) -> None:
        """
        Som para nova posição aberta.
        """
        # Som ascendente
        cls._beep(900, 150)
        cls._beep(1100, 150)

    @classmethod
    def posicao_fechada(cls) -> None:
        """
        Som para posição fechada.
        """
        # Som descendente
        cls._beep(1100, 150)
        cls._beep(700, 200)
