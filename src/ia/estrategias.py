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

        capturas = []
        promocoes = []
        movimentos_seguros = []

        for (linha_origem, coluna_origem), (linha_destino, coluna_destino) in movimentos:
            diff = abs(linha_destino - linha_origem)

            if diff == 2:
                capturas.append(((linha_origem, coluna_origem),
                               (linha_destino, coluna_destino)))
            elif self._leva_a_promocao(jogo, linha_origem, linha_destino):
                promocoes.append(((linha_origem, coluna_origem),
                                (linha_destino, coluna_destino)))
            elif self._eh_movimento_seguro(jogo, linha_destino, coluna_destino):
                movimentos_seguros.append(((linha_origem, coluna_origem),
                                         (linha_destino, coluna_destino)))

        if capturas:
            return self._escolher_melhor_captura(jogo, capturas)
        if promocoes:
            return random.choice(promocoes)
        if movimentos_seguros:
            return random.choice(movimentos_seguros)
        return None

    def _leva_a_promocao(self, jogo: Jogo, linha_origem: int, linha_destino: int) -> bool:
        return linha_destino == 0 or linha_destino == 7

    def _eh_movimento_seguro(self, jogo: Jogo, linha: int, coluna: int) -> bool:
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dir_linha, dir_coluna in direcoes:
            peca_adjacente_linha = linha + dir_linha
            peca_adjacente_coluna = coluna + dir_coluna

            if not self._posicao_valida(peca_adjacente_linha, peca_adjacente_coluna):
                continue

            peca_adjacente = jogo.tabuleiro.obter_peca(
                peca_adjacente_linha, peca_adjacente_coluna
            )

            if peca_adjacente and not peca_adjacente.pertence_ao_jogador(Jogador.JOGADOR2):
                if self._pode_capturar(jogo, peca_adjacente_linha, peca_adjacente_coluna,
                                      linha, coluna):
                    return False

        return True

    def _escolher_melhor_captura(self, jogo: Jogo, capturas: List[Movimento]) -> Movimento:
        """Escolhe a captura que abre mais capturas sequenciais."""
        melhor = None
        max_sequencia = 0

        for movimento in capturas:
            (linha_origem, coluna_origem), (linha_destino, coluna_destino) = movimento
            peca = jogo.tabuleiro.obter_peca(linha_origem, coluna_origem)
            if peca is None:
                continue

            peca_capturada = jogo.tabuleiro.obter_peca(
                (linha_origem + linha_destino) // 2,
                (coluna_origem + coluna_destino) // 2
            )
            tipo_original = peca.tipo

            try:
                if peca_capturada:
                    jogo.tabuleiro.remover_peca(
                        (linha_origem + linha_destino) // 2,
                        (coluna_origem + coluna_destino) // 2
                    )
                if jogo.tabuleiro.mover_peca(
                    linha_origem, coluna_origem, linha_destino, coluna_destino
                ) is None:
                    continue

                jogo.tentar_promover_peca(peca)

                proximas_capturas = jogo.encontrar_capturas_para_peca(
                    linha_destino, coluna_destino
                )

                if len(proximas_capturas) > max_sequencia:
                    max_sequencia = len(proximas_capturas)
                    melhor = movimento
            finally:
                jogo.tabuleiro.mover_peca(
                    linha_destino, coluna_destino, linha_origem, coluna_origem
                )
                peca.tipo = tipo_original
                if peca_capturada:
                    jogo.tabuleiro.colocar_peca(
                        peca_capturada,
                        (linha_origem + linha_destino) // 2,
                        (coluna_origem + coluna_destino) // 2
                    )

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

        pos_apos = jogo.tabuleiro.obter_peca(pos_apos_linha, pos_apos_coluna)
        return pos_apos is None

    def _posicao_valida(self, linha: int, coluna: int) -> bool:
        return (0 <= linha < Tabuleiro.TAMANHO and
                0 <= coluna < Tabuleiro.TAMANHO)


class EstrategiaMinimax(EstrategiaIA):
    """
    Minimax com poda alfa-beta. Avaliação material-based (peça=1, dama=3).
    Reutiliza jogo.desfazer_jogada() para navegar a árvore sem copiar estado.
    """

    VALOR_PECA = 1
    VALOR_DAMA = 3
    VALOR_VITORIA = 10_000

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
        score = 0
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = jogo.tabuleiro.obter_peca(linha, coluna)
                if peca is None:
                    continue
                valor = self.VALOR_DAMA if peca.eh_dama() else self.VALOR_PECA
                if peca.pertence_ao_jogador(jogador_max):
                    score += valor
                else:
                    score -= valor
        return score

    def _encontrar_movimentos_jogador(self, jogo: Jogo, jogador: Jogador) -> List[Movimento]:
        movimentos = []
        jog_orig = jogo.jogador_atual
        jogo.jogador_atual = jogador

        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = jogo.tabuleiro.obter_peca(linha, coluna)
                if peca is None or not peca.pertence_ao_jogador(jogador):
                    continue
                if jogo.em_sequencia_captura:
                    selecionada = jogo.peca_selecionada
                    if selecionada is None or (linha, coluna) != (selecionada.linha, selecionada.coluna):
                        continue
                movs = jogo.obter_movimentos_validos_para_peca(linha, coluna)
                for ml, mc in movs:
                    movimentos.append(((linha, coluna), (ml, mc)))

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
