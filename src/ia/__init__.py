"""
Módulo de IA para o jogo de damas.
Implementa estratégias de IA usando Strategy Pattern.
"""

import random
from typing import List, Tuple
from src.models import Jogador, Tabuleiro
from src.game import Jogo
from src.ia.estrategias import (
    EstrategiaIA,
    EstrategiaFacil,
    EstrategiaNormal,
    EstrategiaMinimax,
    EstrategiaMedia,
    EstrategiaDificil,
)


class IA:
    """
    Classe que implementa IA para jogar damas.

    Usa Strategy Pattern para permitir diferentes níveis de dificuldade.
    Segue OCP/DIP: depende da abstração EstrategiaIA.
    """

    _estrategias = {
        "facil": EstrategiaFacil,
        "normal": EstrategiaNormal,
        "medio": EstrategiaMedia,
        "dificil": EstrategiaDificil,
    }

    def __init__(self, jogo: Jogo, dificuldade: str = "normal",
                 jogador: Jogador = Jogador.JOGADOR2):
        """
        Args:
            jogo: Instância do jogo atual
            dificuldade: "facil" | "normal" | "medio" | "dificil"
            jogador: qual lado a IA controla
        """
        self.jogo = jogo
        self.jogador = jogador
        self.dificuldade = dificuldade
        self._estrategia = self._criar_estrategia(dificuldade)

    def _criar_estrategia(self, dificuldade: str) -> EstrategiaIA:
        estrategia_class = self._estrategias.get(dificuldade, EstrategiaNormal)
        return estrategia_class()

    def alterar_dificuldade(self, dificuldade: str) -> None:
        self.dificuldade = dificuldade
        self._estrategia = self._criar_estrategia(dificuldade)

    def fazer_movimento(self) -> bool:
        """Escolhe e executa um movimento para a IA. Retorna True em sucesso."""
        movimentos = self._encontrar_todos_movimentos()
        if not movimentos:
            return False

        melhor_movimento = self._estrategia.escolher_movimento(self.jogo, movimentos)
        if melhor_movimento is None:
            melhor_movimento = random.choice(movimentos)

        (linha_origem, coluna_origem), (linha_destino, coluna_destino) = melhor_movimento

        if not self.jogo.em_sequencia_captura:
            self.jogo.selecionar_peca(linha_origem, coluna_origem)

        return self.jogo.mover_peca(linha_origem, coluna_origem,
                                    linha_destino, coluna_destino)

    def _encontrar_todos_movimentos(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Encontra todos os movimentos possíveis para a IA no turno atual."""
        movimentos = []

        jogador_original = self.jogo.jogador_atual
        self.jogo.jogador_atual = self.jogador

        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = self.jogo.tabuleiro.obter_peca(linha, coluna)
                if peca is None or not peca.pertence_ao_jogador(self.jogador):
                    continue

                if self.jogo.em_sequencia_captura:
                    selecionada = self.jogo.peca_selecionada
                    if selecionada is None or \
                       (linha, coluna) != (selecionada.linha, selecionada.coluna):
                        continue

                movs_validos = self.jogo.obter_movimentos_validos_para_peca(linha, coluna)
                for mov_linha, mov_coluna in movs_validos:
                    movimentos.append(((linha, coluna), (mov_linha, mov_coluna)))

        self.jogo.jogador_atual = jogador_original
        return movimentos
