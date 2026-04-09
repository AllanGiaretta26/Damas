"""
Módulo de models do jogo de damas.
Exporta todas as classes de domínio.
"""

from src.models.enums import TipoPeca, Jogador, CorPeca
from src.models.peca import Peca
from src.models.tabuleiro import Tabuleiro

__all__ = [
    'TipoPeca',
    'Jogador',
    'CorPeca',
    'Peca',
    'Tabuleiro',
]
