"""
Estratégias de IA para o jogo de damas.
Aplica o Strategy Pattern para permitir diferentes dificuldades (OCP/DIP).
"""

import random
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from src.models import Jogador, Tabuleiro, Peca
from src.game import Jogo


Movimento = Tuple[Tuple[int, int], Tuple[int, int]]


class EstrategiaIA(ABC):
    """Interface base para estratégias de IA (Strategy Pattern)."""

    @abstractmethod
    def escolher_movimento(self, jogo: Jogo, movimentos: List[Movimento]) -> Optional[Movimento]:
        """Escolhe o melhor movimento dentre os disponíveis."""
        pass


class EstrategiaFacil(EstrategiaIA):
    """Estratégia fácil: movimentos completamente aleatórios."""

    def escolher_movimento(self, jogo: Jogo, movimentos: List[Movimento]) -> Optional[Movimento]:
        if not movimentos:
            return None
        return random.choice(movimentos)


class EstrategiaNormal(EstrategiaIA):
    """
    Estratégia normal: prioriza capturas > promoções > movimentos seguros.
    Mantida para compatibilidade e como opção intermediária leve.
    """

    def escolher_movimento(self, jogo: Jogo, movimentos: List[Movimento]) -> Optional[Movimento]:
        if not movimentos:
            return None

        jogador = jogo.jogador_atual
        capturas = []
        promocoes = []
        movimentos_seguros = []

        for (linha_origem, coluna_origem), (linha_destino, coluna_destino) in movimentos:
            diff = abs(linha_destino - linha_origem)

            if diff == 2:
                capturas.append(((linha_origem, coluna_origem),
                               (linha_destino, coluna_destino)))
            elif self._leva_a_promocao(linha_destino):
                promocoes.append(((linha_origem, coluna_origem),
                                (linha_destino, coluna_destino)))
            elif self._eh_movimento_seguro(jogo, linha_destino, coluna_destino, jogador):
                movimentos_seguros.append(((linha_origem, coluna_origem),
                                         (linha_destino, coluna_destino)))

        if capturas:
            return self._escolher_melhor_captura(jogo, capturas)
        if promocoes:
            return random.choice(promocoes)
        if movimentos_seguros:
            return random.choice(movimentos_seguros)
        return random.choice(movimentos)

    @staticmethod
    def _leva_a_promocao(linha_destino: int) -> bool:
        return linha_destino == 0 or linha_destino == 7

    def _eh_movimento_seguro(self, jogo: Jogo, linha: int, coluna: int,
                              jogador: Jogador) -> bool:
        for dir_linha, dir_coluna in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            adj_linha = linha + dir_linha
            adj_coluna = coluna + dir_coluna

            if not self._posicao_valida(adj_linha, adj_coluna):
                continue

            peca_adj = jogo.tabuleiro.obter_peca(adj_linha, adj_coluna)
            if peca_adj and not peca_adj.pertence_ao_jogador(jogador):
                if self._pode_capturar(jogo, adj_linha, adj_coluna, linha, coluna):
                    return False

        return True

    def _escolher_melhor_captura(self, jogo: Jogo, capturas: List[Movimento]) -> Movimento:
        """Escolhe a captura que abre mais sequências usando o sistema de undo."""
        melhor = None
        max_sequencia = -1

        for movimento in capturas:
            (lo, co), (ld, cd) = movimento
            if not jogo.mover_peca(lo, co, ld, cd):
                continue
            proximas = jogo.encontrar_capturas_para_peca(ld, cd)
            sequencia = len(proximas)
            jogo.desfazer_jogada()

            if sequencia > max_sequencia:
                max_sequencia = sequencia
                melhor = movimento

        return melhor if melhor else random.choice(capturas)

    def _pode_capturar(self, jogo: Jogo, peca_linha: int, peca_coluna: int,
                       alvo_linha: int, alvo_coluna: int) -> bool:
        peca = jogo.tabuleiro.obter_peca(peca_linha, peca_coluna)
        if peca is None:
            return False

        dir_linha = 1 if alvo_linha > peca_linha else -1
        dir_coluna = 1 if alvo_coluna > peca_coluna else -1
        pos_apos_linha = alvo_linha + dir_linha
        pos_apos_coluna = alvo_coluna + dir_coluna

        if not self._posicao_valida(pos_apos_linha, pos_apos_coluna):
            return False

        return jogo.tabuleiro.obter_peca(pos_apos_linha, pos_apos_coluna) is None

    @staticmethod
    def _posicao_valida(linha: int, coluna: int) -> bool:
        return 0 <= linha < Tabuleiro.TAMANHO and 0 <= coluna < Tabuleiro.TAMANHO


class EstrategiaMinimax(EstrategiaIA):
    """
    Minimax com poda alfa-beta. Avaliação material + posicional.
    Reutiliza jogo.desfazer_jogada() para navegar a árvore sem copiar estado.
    """

    VALOR_PECA = 1
    VALOR_DAMA = 3
    VALOR_VITORIA = 10_000
    BONUS_CENTRO = 0.05
    BONUS_GUARDA_FINAL = 0.3

    def __init__(self, profundidade: int):
        self.profundidade = profundidade

    def escolher_movimento(self, jogo: Jogo, movimentos: List[Movimento]) -> Optional[Movimento]:
        if not movimentos:
            return None

        jogador_max = jogo.jogador_atual
        alfa = -float('inf')
        beta = float('inf')
        melhor_score = -float('inf')
        melhor_mov = movimentos[0]

        for mov in self._ordenar_movimentos(movimentos):
            (lo, co), (ld, cd) = mov
            if not jogo.mover_peca(lo, co, ld, cd):
                continue
            score = self._minimax(jogo, self.profundidade - 1, alfa, beta, jogador_max)
            jogo.desfazer_jogada()

            if score > melhor_score:
                melhor_score = score
                melhor_mov = mov
            alfa = max(alfa, melhor_score)

        return melhor_mov

    def _minimax(self, jogo: Jogo, profundidade: int,
                 alfa: float, beta: float, jogador_max: Jogador) -> float:
        fim, vencedor = jogo.verificar_fim_de_jogo()
        if fim:
            return self.VALOR_VITORIA if vencedor == jogador_max else -self.VALOR_VITORIA
        if profundidade == 0:
            return self._avaliar(jogo, jogador_max)

        jogador_atual = jogo.jogador_atual
        maximizando = (jogador_atual == jogador_max)
        movimentos = self._encontrar_movimentos_jogador(jogo, jogador_atual)

        if not movimentos:
            return -self.VALOR_VITORIA if maximizando else self.VALOR_VITORIA

        if maximizando:
            melhor = -float('inf')
            for mov in movimentos:
                (lo, co), (ld, cd) = mov
                if not jogo.mover_peca(lo, co, ld, cd):
                    continue
                score = self._minimax(jogo, profundidade - 1, alfa, beta, jogador_max)
                jogo.desfazer_jogada()
                if score > melhor:
                    melhor = score
                if melhor > alfa:
                    alfa = melhor
                if beta <= alfa:
                    break
            return melhor
        else:
            pior = float('inf')
            for mov in movimentos:
                (lo, co), (ld, cd) = mov
                if not jogo.mover_peca(lo, co, ld, cd):
                    continue
                score = self._minimax(jogo, profundidade - 1, alfa, beta, jogador_max)
                jogo.desfazer_jogada()
                if score < pior:
                    pior = score
                if pior < beta:
                    beta = pior
                if beta <= alfa:
                    break
            return pior

    def _avaliar(self, jogo: Jogo, jogador_max: Jogador) -> float:
        score = 0.0
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = jogo.tabuleiro.obter_peca(linha, coluna)
                if peca is None:
                    continue
                valor = float(self.VALOR_DAMA if peca.eh_dama() else self.VALOR_PECA)
                valor += self._bonus_posicao(peca, linha, coluna)
                if peca.pertence_ao_jogador(jogador_max):
                    score += valor
                else:
                    score -= valor
        return score

    def _bonus_posicao(self, peca: Peca, linha: int, coluna: int) -> float:
        distancia_centro = abs(3.5 - linha) + abs(3.5 - coluna)
        bonus = (7.0 - distancia_centro) * self.BONUS_CENTRO
        if not peca.eh_dama():
            if peca.jogador == Jogador.JOGADOR1 and linha == 7:
                bonus += self.BONUS_GUARDA_FINAL
            elif peca.jogador == Jogador.JOGADOR2 and linha == 0:
                bonus += self.BONUS_GUARDA_FINAL
        return bonus

    def _encontrar_movimentos_jogador(self, jogo: Jogo, jogador: Jogador) -> List[Movimento]:
        movimentos = []
        jog_orig = jogo.jogador_atual
        jogo.jogador_atual = jogador
        try:
            for linha in range(Tabuleiro.TAMANHO):
                for coluna in range(Tabuleiro.TAMANHO):
                    peca = jogo.tabuleiro.obter_peca(linha, coluna)
                    if peca is None or not peca.pertence_ao_jogador(jogador):
                        continue
                    if jogo.em_sequencia_captura:
                        sel = jogo.peca_selecionada
                        if sel is None or (linha, coluna) != (sel.linha, sel.coluna):
                            continue
                    movs = jogo.obter_movimentos_validos_para_peca(linha, coluna)
                    for ml, mc in movs:
                        movimentos.append(((linha, coluna), (ml, mc)))
        finally:
            jogo.jogador_atual = jog_orig
        return movimentos

    def _ordenar_movimentos(self, movimentos: List[Movimento]) -> List[Movimento]:
        """Capturas primeiro — melhora a poda alfa-beta."""
        def chave(mov: Movimento) -> int:
            (lo, _), (ld, _) = mov
            return 0 if abs(ld - lo) == 2 else 1
        return sorted(movimentos, key=chave)


class EstrategiaMedia(EstrategiaMinimax):
    """Minimax profundidade 3."""

    def __init__(self):
        super().__init__(profundidade=3)


class EstrategiaDificil(EstrategiaMinimax):
    """Minimax profundidade 5."""

    def __init__(self):
        super().__init__(profundidade=5)
