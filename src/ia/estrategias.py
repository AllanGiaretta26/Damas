"""
Estratégias de IA para o jogo de damas.
Aplica o Strategy Pattern para permitir diferentes dificuldades (OCP/DIP).
"""

import random
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from src.models import Jogador, Tabuleiro, Peca
from src.game import Jogo


class EstrategiaIA(ABC):
    """
    Interface base para estratégias de IA (Strategy Pattern).
    
    Segue OCP: aberto para extensão (novas estratégias), 
    fechado para modificação.
    """

    @abstractmethod
    def escolher_movimento(self, jogo: Jogo, movimentos: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Escolhe o melhor movimento dentre os disponíveis.
        
        Args:
            jogo: Instância do jogo atual
            movimentos: Lista de movimentos possíveis no formato 
                       ((linha_origem, coluna_origem), (linha_destino, coluna_destino))
            
        Returns:
            O movimento escolhido ou None se não houver preferência
        """
        pass


class EstrategiaFacil(EstrategiaIA):
    """
    Estratégia fácil: movimentos completamente aleatórios.
    """

    def escolher_movimento(self, jogo: Jogo, movimentos: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Escolhe um movimento aleatório."""
        if not movimentos:
            return None
        return random.choice(movimentos)


class EstrategiaNormal(EstrategiaIA):
    """
    Estratégia normal: prioriza capturas > promoções > movimentos seguros.
    """

    def escolher_movimento(self, jogo: Jogo, movimentos: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Avalia os movimentos e retorna o melhor.
        
        Prioridade:
        1. Capturas (especialmente sequenciais)
        2. Promoções
        3. Movimentos seguros
        4. Aleatório
        """
        if not movimentos:
            return None

        capturas = []
        promocoes = []
        movimentos_seguros = []

        for (linha_origem, coluna_origem), (linha_destino, coluna_destino) in movimentos:
            diff = abs(linha_destino - linha_origem)

            # Verificar se é captura
            if diff == 2:
                capturas.append(((linha_origem, coluna_origem),
                               (linha_destino, coluna_destino)))

            # Verificar se leva à promoção
            elif self._leva_a_promocao(jogo, linha_origem, linha_destino):
                promocoes.append(((linha_origem, coluna_origem),
                                (linha_destino, coluna_destino)))

            # Verificar se é seguro
            elif self._eh_movimento_seguro(jogo, linha_destino, coluna_destino):
                movimentos_seguros.append(((linha_origem, coluna_origem),
                                         (linha_destino, coluna_destino)))

        # Priorizar: capturas > promoções > movimentos seguros > aleatório
        if capturas:
            return self._escolher_melhor_captura(jogo, capturas)

        if promocoes:
            return random.choice(promocoes)

        if movimentos_seguros:
            return random.choice(movimentos_seguros)

        return None

    def _leva_a_promocao(self, jogo: Jogo, linha_origem: int, linha_destino: int) -> bool:
        """Verifica se o movimento leva à promoção."""
        peca = jogo.tabuleiro.obter_peca(linha_origem, 0)  # Precisamos da coluna
        # Simplificação: verificar se destino é linha de promoção
        return linha_destino == 0 or linha_destino == 7

    def _eh_movimento_seguro(self, jogo: Jogo, linha: int, coluna: int) -> bool:
        """Verifica se uma posição de destino é segura."""
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

    def _escolher_melhor_captura(self, jogo: Jogo, capturas: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Escolhe a melhor captura, preferindo as que levam a mais capturas."""
        melhor = None
        max_sequencia = 0

        for movimento in capturas:
            (linha_origem, coluna_origem), (linha_destino, coluna_destino) = movimento

            # Simular movimento
            peca = jogo.tabuleiro.obter_peca(linha_origem, coluna_origem)
            if peca is None:
                continue

            peca_capturada = jogo.tabuleiro.obter_peca(
                (linha_origem + linha_destino) // 2,
                (coluna_origem + coluna_destino) // 2
            )
            tipo_original = peca.tipo

            try:
                # Fazer movimento temporário
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

                # Contar quantas capturas adicionais são possíveis
                proximas_capturas = jogo.encontrar_capturas_para_peca(
                    linha_destino, coluna_destino
                )

                if len(proximas_capturas) > max_sequencia:
                    max_sequencia = len(proximas_capturas)
                    melhor = movimento
            finally:
                # Restaurar estado
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
        """Verifica se uma peça pode capturar na posição alvo."""
        peca = jogo.tabuleiro.obter_peca(peca_linha, peca_coluna)
        if peca is None:
            return False

        # Calcular direção
        dir_linha = 1 if alvo_linha > peca_linha else -1
        dir_coluna = 1 if alvo_coluna > peca_coluna else -1

        # Posição após captura
        pos_apos_linha = alvo_linha + dir_linha
        pos_apos_coluna = alvo_coluna + dir_coluna

        # Verificar se é movimento válido
        if not self._posicao_valida(pos_apos_linha, pos_apos_coluna):
            return False

        pos_apos = jogo.tabuleiro.obter_peca(pos_apos_linha, pos_apos_coluna)
        if pos_apos is not None:
            return False

        return True

    def _posicao_valida(self, linha: int, coluna: int) -> bool:
        """Verifica se uma posição está dentro do tabuleiro."""
        return (0 <= linha < Tabuleiro.TAMANHO and
                0 <= coluna < Tabuleiro.TAMANHO)


class EstrategiaDificil(EstrategiaNormal):
    """
    Estratégia difícil: mesma que normal, mas com avaliação mais profunda.
    Pode ser estendida no futuro com minimax ou alpha-beta pruning.
    """

    def escolher_movimento(self, jogo: Jogo, movimentos: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Escolhe movimento com avaliação mais profunda.
        Por enquanto, usa estratégia normal com preferência por centro.
        """
        if not movimentos:
            return None

        # Usar estratégia normal
        escolha_normal = super().escolher_movimento(jogo, movimentos)
        if escolha_normal:
            return escolha_normal

        # Preferir movimentos para o centro do tabuleiro
        return self._preferir_centro(jogo, movimentos)

    def _preferir_centro(self, jogo: Jogo, movimentos: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Prefere movimentos que levam ao centro do tabuleiro."""
        centro = (3.5, 3.5)
        melhor_movimento = None
        menor_distancia = float('inf')

        for movimento in movimentos:
            (linha_origem, coluna_origem), (linha_destino, coluna_destino) = movimento
            
            # Calcular distância ao centro
            distancia = abs(linha_destino - centro[0]) + abs(coluna_destino - centro[1])
            
            if distancia < menor_distancia:
                menor_distancia = distancia
                melhor_movimento = movimento

        return melhor_movimento if melhor_movimento else random.choice(movimentos)
