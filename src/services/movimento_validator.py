"""
Serviço de validação de movimentos no jogo de damas.
Responsável por aplicar o Single Responsibility Principle (SRP).
"""

from typing import List, Tuple
from src.models.tabuleiro import Tabuleiro
from src.models.peca import Peca
from src.models.enums import Jogador, TipoPeca


class MovimentoValidator:
    """
    Valida movimentos no jogo de damas.
    
    Responsabilidades:
    - Calcular movimentos válidos para uma peça
    - Validar movimentos simples
    - Encontrar capturas disponíveis
    
    Segue SRP: apenas valida, não modifica estado do jogo.
    """

    def __init__(self, tabuleiro: Tabuleiro):
        """Inicializa o validador com referência ao tabuleiro."""
        self._tabuleiro = tabuleiro

    def calcular_movimentos_validos(self, linha: int, coluna: int, 
                                    jogador_atual: Jogador,
                                    em_sequencia_captura: bool = False,
                                    peca_selecionada: Peca = None) -> List[Tuple[int, int]]:
        """
        Calcula todos os movimentos válidos para uma peça.
        
        Args:
            linha: Linha da peça
            coluna: Coluna da peça
            jogador_atual: Jogador cujo turno é agora
            em_sequencia_captura: Se está em meio a uma sequência de capturas
            peca_selecionada: Peça atualmente selecionada (para validação)
        """
        peca = self._tabuleiro.obter_peca(linha, coluna)
        if peca is None or not peca.pertence_ao_jogador(jogador_atual):
            return []

        # Se está em sequência de captura, só permite capturas da mesma peça
        if em_sequencia_captura:
            if peca_selecionada is None:
                return []
            if (linha, coluna) != (peca_selecionada.linha, peca_selecionada.coluna):
                return []
            return self.encontrar_capturas(linha, coluna)

        # Se o jogador tem capturas disponíveis, só permite capturas
        capturas = self.encontrar_capturas(linha, coluna)
        if self._jogador_tem_capturas(jogador_atual):
            return capturas

        # Movimento simples
        return self._calcular_movimentos_simples(peca)

    def _calcular_movimentos_simples(self, peca: Peca) -> List[Tuple[int, int]]:
        """Calcula movimentos simples (não captura) para uma peça.
        
        Jogador 1 (Vermelho): sobe no tabuleiro (dir_linha = -1)
        Jogador 2 (Azul): desce no tabuleiro (dir_linha = +1)
        """
        movimentos = []
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dir_linha, dir_coluna in direcoes:
            nova_linha = peca.linha + dir_linha
            nova_coluna = peca.coluna + dir_coluna

            # Peças comuns só se movem para frente
            if peca.tipo == TipoPeca.PECA:
                # J1 sobe (linha diminui), J2 desce (linha aumenta)
                if peca.jogador == Jogador.JOGADOR1 and dir_linha != -1:
                    continue
                if peca.jogador == Jogador.JOGADOR2 and dir_linha != 1:
                    continue

            if self._movimento_simples_valido(nova_linha, nova_coluna):
                movimentos.append((nova_linha, nova_coluna))

        return movimentos

    def _movimento_simples_valido(self, linha: int, coluna: int) -> bool:
        """Verifica se um movimento simples é válido."""
        if not self._posicao_valida(linha, coluna):
            return False
        if not self._tabuleiro.eh_casa_preta_publico(linha, coluna):
            return False
        if self._tabuleiro.obter_peca(linha, coluna) is not None:
            return False
        return True

    def encontrar_capturas(self, linha: int, coluna: int) -> List[Tuple[int, int]]:
        """
        Encontra todos os movimentos de captura válidos para uma peça.
        
        Jogador 1 (Vermelho): captura subindo (dir_linha = -1)
        Jogador 2 (Azul): captura descendo (dir_linha = +1)

        Args:
            linha: Linha da peça
            coluna: Coluna da peça

        Returns:
            Lista de tuplas (linha_destino, coluna_destino) para capturas válidas
        """
        peca = self._tabuleiro.obter_peca(linha, coluna)
        if peca is None:
            return []

        capturas = []
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dir_linha, dir_coluna in direcoes:
            nova_linha = linha + dir_linha * 2
            nova_coluna = coluna + dir_coluna * 2

            # Peças comuns só capturam para frente
            if peca.tipo == TipoPeca.PECA:
                # J1 captura subindo, J2 captura descendo
                if peca.jogador == Jogador.JOGADOR1 and dir_linha != -1:
                    continue
                if peca.jogador == Jogador.JOGADOR2 and dir_linha != 1:
                    continue

            # Verificar se a captura é válida
            peca_alvo = self._tabuleiro.obter_peca(
                linha + dir_linha, coluna + dir_coluna
            )

            if (self._movimento_simples_valido(nova_linha, nova_coluna) and
                peca_alvo is not None and
                not peca_alvo.pertence_ao_jogador(peca.jogador)):
                capturas.append((nova_linha, nova_coluna))

        return capturas

    def _jogador_tem_capturas(self, jogador: Jogador) -> bool:
        """Verifica se o jogador possui alguma captura obrigatória."""
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = self._tabuleiro.obter_peca(linha, coluna)
                if peca and peca.pertence_ao_jogador(jogador):
                    if self.encontrar_capturas(linha, coluna):
                        return True
        return False

    def _posicao_valida(self, linha: int, coluna: int) -> bool:
        """Verifica se uma posição está dentro do tabuleiro."""
        return (0 <= linha < Tabuleiro.TAMANHO and
                0 <= coluna < Tabuleiro.TAMANHO)

    def tem_movimentos_disponiveis(self, jogador: Jogador) -> bool:
        """Verifica se um jogador tem movimentos disponíveis."""
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = self._tabuleiro.obter_peca(linha, coluna)
                if peca and peca.pertence_ao_jogador(jogador):
                    movimentos = self.calcular_movimentos_validos(
                        linha, coluna, jogador
                    )
                    if movimentos:
                        return True
        return False
