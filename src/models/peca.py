"""
Módulo que contém a classe Peca.
Representa uma peça do jogo de damas.
"""

from src.models.enums import TipoPeca, Jogador


class Peca:
    """
    Representa uma peça do jogo de damas.
    
    Responsabilidades:
    - Manter estado da peça (tipo, jogador, posição)
    - Promover a dama
    - Atualizar posição
    
    Segue SRP: uma peça apenas gerencia seu próprio estado.
    """

    def __init__(self, jogador: Jogador, linha: int, coluna: int):
        """Inicializa uma peça."""
        self.jogador = jogador
        self.tipo = TipoPeca.PECA
        self.linha = linha
        self.coluna = coluna

    def promover(self) -> None:
        """Promove uma peça comum para dama."""
        self.tipo = TipoPeca.DAMA

    def atualizar_posicao(self, nova_linha: int, nova_coluna: int) -> None:
        """Move a peça para uma nova posição."""
        self.linha = nova_linha
        self.coluna = nova_coluna

    def eh_dama(self) -> bool:
        """Retorna True se a peça é uma dama."""
        return self.tipo == TipoPeca.DAMA

    def pertence_ao_jogador(self, jogador: Jogador) -> bool:
        """Verifica se a peça pertence a um jogador específico."""
        return self.jogador == jogador

    def __repr__(self) -> str:
        tipo = "D" if self.eh_dama() else "P"
        jogador = "1" if self.jogador == Jogador.JOGADOR1 else "2"
        return f"{jogador}{tipo}"
