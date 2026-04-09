"""
Enumerações utilizadas no jogo de damas.
"""

from enum import Enum


class TipoPeca(Enum):
    """Enumeração para os tipos de peças."""
    PECA = 1
    DAMA = 2


class Jogador(Enum):
    """Enumeração para os jogadores."""
    JOGADOR1 = 1
    JOGADOR2 = 2


class CorPeca(Enum):
    """Enumeração para cores das peças na interface."""
    JOGADOR1 = "#FF0000"
    JOGADOR2 = "#0000FF"
    DAMA = "#FFD700"
