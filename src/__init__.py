"""
Jogo de Damas em Python
Pacote src contendo toda a lógica e interface do jogo.

Estrutura refatorada seguindo princípios SOLID e Clean Code:
- models: Classes de domínio (Peca, Tabuleiro, enums)
- services: Serviços especializados (validação, captura, promoção)
- ia: Inteligência artificial com Strategy Pattern
- gui: Interface gráfica separada em renderização e gerenciamento
"""

__version__ = "2.0.0"
__author__ = "Desenvolvimento em Python"
__description__ = "Um jogo de damas completo com interface gráfica em tkinter, refatorado com SOLID e Clean Code"

__all__ = [
    'Jogo',
    'Peca',
    'Tabuleiro',
    'Jogador',
    'TipoPeca',
    'GUIJogo',
    'IA',
]
