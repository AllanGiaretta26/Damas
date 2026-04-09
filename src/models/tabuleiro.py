"""
Módulo que contém a classe Tabuleiro.
Representa o tabuleiro do jogo de damas.
"""

from typing import List, Optional
from src.models.enums import Jogador
from src.models.peca import Peca


class Tabuleiro:
    """
    Representa o tabuleiro do jogo de damas.
    
    Responsabilidades:
    - Gerenciar o estado das casas (matriz 8x8)
    - Colocar, mover e remover peças
    - Validar posições
    - Configurar posição inicial das peças
    
    Segue SRP: tabuleiro apenas gerencia o estado das casas.
    """

    TAMANHO = 8

    def __init__(self):
        """Inicializa o tabuleiro com as peças na posição inicial."""
        self._casas: List[List[Optional[Peca]]] = [
            [None for _ in range(self.TAMANHO)] 
            for _ in range(self.TAMANHO)
        ]
        self._configurar_posicao_inicial()

    def _configurar_posicao_inicial(self) -> None:
        """Coloca as peças na posição inicial do jogo.
        
        Jogador 2 (Azul): linhas 0-2 (parte superior)
        Jogador 1 (Vermelho): linhas 5-7 (parte inferior)
        """
        # Peças do Jogador 2 (linhas 0-2) - PARTE SUPERIOR
        for linha in range(3):
            for coluna in range(self.TAMANHO):
                if self._eh_casa_preta(linha, coluna):
                    self.colocar_peca(Peca(Jogador.JOGADOR2, linha, coluna), linha, coluna)

        # Peças do Jogador 1 (linhas 5-7) - PARTE INFERIOR
        for linha in range(5, self.TAMANHO):
            for coluna in range(self.TAMANHO):
                if self._eh_casa_preta(linha, coluna):
                    self.colocar_peca(Peca(Jogador.JOGADOR1, linha, coluna), linha, coluna)

    def obter_peca(self, linha: int, coluna: int) -> Optional[Peca]:
        """Obtém a peça em uma posição específica."""
        if self._posicao_valida(linha, coluna):
            return self._casas[linha][coluna]
        return None

    def colocar_peca(self, peca: Peca, linha: int, coluna: int) -> None:
        """Coloca uma peça em uma posição."""
        if self._posicao_valida(linha, coluna):
            self._casas[linha][coluna] = peca
            peca.atualizar_posicao(linha, coluna)

    def mover_peca(self, linha_origem: int, coluna_origem: int,
                   linha_destino: int, coluna_destino: int) -> Optional[Peca]:
        """
        Move uma peça dentro do tabuleiro.
        
        Returns:
            A peça movida ou None se o movimento falhar.
        """
        if not (self._posicao_valida(linha_origem, coluna_origem) and
                self._posicao_valida(linha_destino, coluna_destino)):
            return None

        peca = self.obter_peca(linha_origem, coluna_origem)
        if peca is None or self.obter_peca(linha_destino, coluna_destino) is not None:
            return None

        self._casas[linha_origem][coluna_origem] = None
        self._casas[linha_destino][coluna_destino] = peca
        peca.atualizar_posicao(linha_destino, coluna_destino)
        return peca

    def remover_peca(self, linha: int, coluna: int) -> Optional[Peca]:
        """Remove e retorna uma peça de uma posição."""
        if self._posicao_valida(linha, coluna):
            peca = self._casas[linha][coluna]
            self._casas[linha][coluna] = None
            return peca
        return None

    def _posicao_valida(self, linha: int, coluna: int) -> bool:
        """Verifica se uma posição está dentro do tabuleiro."""
        return 0 <= linha < self.TAMANHO and 0 <= coluna < self.TAMANHO

    def _eh_casa_preta(self, linha: int, coluna: int) -> bool:
        """Verifica se a casa é preta (onde as peças podem estar)."""
        return (linha + coluna) % 2 == 1

    def eh_casa_preta_publico(self, linha: int, coluna: int) -> bool:
        """Interface pública para verificar casa preta."""
        return self._eh_casa_preta(linha, coluna)

    def resetar(self) -> None:
        """Reseta o tabuleiro para a posição inicial."""
        self._casas = [[None for _ in range(self.TAMANHO)] 
                      for _ in range(self.TAMANHO)]
        self._configurar_posicao_inicial()

    def obter_todas_pecas(self, jogador: Jogador) -> List[Peca]:
        """Retorna todas as peças de um jogador."""
        pecas = []
        for linha in range(self.TAMANHO):
            for coluna in range(self.TAMANHO):
                peca = self.obter_peca(linha, coluna)
                if peca and peca.pertence_ao_jogador(jogador):
                    pecas.append(peca)
        return pecas

    def contar_pecas(self, jogador: Jogador) -> int:
        """Conta quantas peças um jogador tem no tabuleiro."""
        return len(self.obter_todas_pecas(jogador))

    def obter_matriz_casas(self) -> List[List[Optional[Peca]]]:
        """Retorna a matriz completa de casas (para a GUI)."""
        return self._casas
