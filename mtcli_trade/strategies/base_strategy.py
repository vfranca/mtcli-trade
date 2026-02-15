"""
Interface base para estratégias de envio de ordem.
"""

from abc import ABC, abstractmethod


class BaseOrderStrategy(ABC):
    """
    Interface Strategy.
    """

    @abstractmethod
    def definir_tipo_ordem(self, controller):
        """
        Define tipo de ordem MT5.
        """

    @abstractmethod
    def definir_preco(self, controller, tick, preco_input):
        """
        Define preço da ordem.
        """
