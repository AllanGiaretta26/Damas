"""
Jogo de Damas em Python
Pacote src contendo toda a lógica e interface do jogo.
"""

__version__ = "1.0.0"
__author__ = "Desenvolvimento em Python"
__description__ = "Um jogo de damas completo com interface gráfica em tkinter"

from src.game import (
    Jogo,
    Peca,
    Tabuleiro,
    Jogador,
    TipoPeca
)

from src.gui import GUIJogo
from src.ia import IA

__all__ = [
    'Jogo',
    'Peca',
    'Tabuleiro',
    'Jogador',
    'TipoPeca',
    'GUIJogo',
    'IA',
]
