"""
Módulo de IA para o jogo de damas.
Implementa estratégias de IA usando Strategy Pattern.
"""

from typing import List, Tuple, Optional
from src.models import Jogador, Tabuleiro
from src.game import Jogo
from src.ia.estrategias import EstrategiaIA, EstrategiaFacil, EstrategiaNormal, EstrategiaDificil


class IA:
    """
    Classe que implementa IA para jogar damas.
    
    Usa Strategy Pattern para permitir diferentes níveis de dificuldade.
    Segue OCP: fácil adicionar novas estratégias.
    Segue DIP: depende da abstração EstrategiaIA, não de implementações.
    """

    # Factory de estratégias
    _estrategias = {
        "facil": EstrategiaFacil,
        "normal": EstrategiaNormal,
        "dificil": EstrategiaDificil,
    }

    def __init__(self, jogo: Jogo, dificuldade: str = "normal"):
        """
        Inicializa a IA.
        
        Args:
            jogo: Instância do jogo atual
            dificuldade: Nível de dificuldade ("facil", "normal", "dificil")
        """
        self.jogo = jogo
        self.jogador = Jogador.JOGADOR2
        self.dificuldade = dificuldade
        self._estrategia = self._criar_estrategia(dificuldade)

    def _criar_estrategia(self, dificuldade: str) -> EstrategiaIA:
        """Factory method para criar estratégia baseada na dificuldade."""
        estrategia_class = self._estrategias.get(dificuldade, EstrategiaNormal)
        return estrategia_class()

    def alterar_dificuldade(self, dificuldade: str) -> None:
        """Altera a dificuldade da IA em runtime."""
        self.dificuldade = dificuldade
        self._estrategia = self._criar_estrategia(dificuldade)

    def fazer_movimento(self) -> bool:
        """
        Faz um movimento para a IA.
        
        Returns:
            True se um movimento foi feito com sucesso
        """
        # Encontrar todos os movimentos possíveis
        movimentos = self._encontrar_todos_movimentos()

        if not movimentos:
            return False

        # Usar estratégia para escolher melhor movimento
        melhor_movimento = self._estrategia.escolher_movimento(self.jogo, movimentos)

        if melhor_movimento is None:
            # Se não conseguir avaliar, fazer movimento aleatório
            melhor_movimento = self._estrategia.escolher_movimento(
                self.jogo, movimentos
            )
            if melhor_movimento is None:
                import random
                melhor_movimento = random.choice(movimentos)

        # Executar movimento
        (linha_origem, coluna_origem), (linha_destino, coluna_destino) = melhor_movimento

        # Se estamos em captura em sequência, não precisa selecionar
        if not self.jogo.em_sequencia_captura:
            self.jogo.selecionar_peca(linha_origem, coluna_origem)
        
        return self.jogo.mover_peca(linha_origem, coluna_origem,
                                   linha_destino, coluna_destino)

    def _encontrar_todos_movimentos(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Encontra todos os movimentos possíveis para a IA.
        
        Returns:
            Lista de tuplas ((linha_origem, coluna_origem), (linha_destino, coluna_destino))
        """
        movimentos = []

        # Temporariamente mudar o jogador atual para a IA
        jogador_original = self.jogo.jogador_atual
        self.jogo.jogador_atual = self.jogador

        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = self.jogo.tabuleiro.obter_peca(linha, coluna)
                if peca and peca.pertence_ao_jogador(self.jogador):
                    # Se em sequência de captura, só pode mover essa peça
                    if self.jogo.em_sequencia_captura:
                        if self.jogo.peca_selecionada and \
                           (linha, coluna) != (self.jogo.peca_selecionada.linha,
                                              self.jogo.peca_selecionada.coluna):
                            continue

                    # Encontrar movimentos válidos para essa peça
                    # Usar método público do jogo (agora com jogador correto)
                    movs_validos = self.jogo.obter_movimentos_validos_para_peca(linha, coluna)
                    for mov_linha, mov_coluna in movs_validos:
                        movimentos.append(((linha, coluna), (mov_linha, mov_coluna)))

        # Restaurar jogador original
        self.jogo.jogador_atual = jogador_original

        return movimentos

    def fazer_movimento(self) -> bool:
        """
        Faz um movimento para a IA.
        
        Returns:
            True se um movimento foi feito com sucesso
        """
        # Encontrar todos os movimentos possíveis
        movimentos = self._encontrar_todos_movimentos()

        if not movimentos:
            return False

        # Usar estratégia para escolher melhor movimento
        melhor_movimento = self._estrategia.escolher_movimento(self.jogo, movimentos)

        if melhor_movimento is None:
            # Se não conseguir avaliar, fazer movimento aleatório
            import random
            melhor_movimento = random.choice(movimentos)

        # Executar movimento
        (linha_origem, coluna_origem), (linha_destino, coluna_destino) = melhor_movimento

        # Se estamos em captura em sequência, não precisa selecionar
        if not self.jogo.em_sequencia_captura:
            self.jogo.selecionar_peca(linha_origem, coluna_origem)

        return self.jogo.mover_peca(linha_origem, coluna_origem,
                                   linha_destino, coluna_destino)
