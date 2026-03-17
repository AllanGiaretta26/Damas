"""
Módulo de IA para o jogo de damas.
Implementa estratégias simples de IA para jogar contra o computador.
"""

import random
from typing import List, Tuple, Optional
from src.game import Jogo, Jogador, Tabuleiro


class IA:
    """
    Classe que implementa IA simples para jogar damas.
    
    Estratégia:
    1. Prioriza capturas (especialmente múltiplas)
    2. Tenta promover peças
    3. Evita perder peças
    4. Caso contrário, move aleatoriamente
    """
    
    def __init__(self, jogo: Jogo):
        """Inicializa a IA."""
        self.jogo = jogo
        self.jogador = Jogador.JOGADOR2
    
    def fazer_movimento(self) -> bool:
        """
        Faz um movimento para a IA.
        
        Retorna True se um movimento foi feito com sucesso.
        """
        # Encontrar todos os movimentos possíveis
        movimentos = self._encontrar_todos_movimentos()
        
        if not movimentos:
            return False
        
        # Avaliar e escolher o melhor movimento
        melhor_movimento = self._avaliar_movimentos(movimentos)
        
        if melhor_movimento is None:
            # Se não conseguir avaliar, fazer movimento aleatório
            melhor_movimento = random.choice(movimentos)
        
        # Executar movimento
        (linha_origem, coluna_origem), (linha_destino, coluna_destino) = melhor_movimento
        
        # Se stamos em captura em sequência
        if self.jogo.em_sequencia_captura:
            self.jogo.mover_peca(linha_origem, coluna_origem,
                                linha_destino, coluna_destino)
        else:
            # Selecionar peça e mover
            self.jogo.selecionar_peca(linha_origem, coluna_origem)
            self.jogo.mover_peca(linha_origem, coluna_origem,
                                linha_destino, coluna_destino)
        
        return True
    
    def _encontrar_todos_movimentos(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Encontra todos os movimentos possíveis para a IA.
        
        Retorna lista de tuplas ((linha_origem, coluna_origem), (linha_destino, coluna_destino))
        """
        movimentos = []
        
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = self.jogo.tabuleiro.obter_peca(linha, coluna)
                if peca and peca.jogador == self.jogador:
                    # Encontrar movimentos validis para essa peça
                    movs_validos = self.jogo._calcular_movimentos_validos(linha, coluna)
                    for mov_linha, mov_coluna in movs_validos:
                        movimentos.append(((linha, coluna), (mov_linha, mov_coluna)))
        
        return movimentos
    
    def _avaliar_movimentos(self, movimentos: List) -> Optional[Tuple]:
        """
        Avalia os movimentos e retorna o melhor.
        
        Estratégia:
        1. Movimentos de captura (múltiplas > simples)
        2. Movimentos que levam à promoção
        3. Movimentos seguros
        """
        capturas = []
        promocoes = []
        movimentos_seguros = []
        
        for (linha_origem, coluna_origem), (linha_destino, coluna_destino) in movimentos:
            peca = self.jogo.tabuleiro.obter_peca(linha_origem, coluna_origem)
            diff = abs(linha_destino - linha_origem)
            
            # Verificar se é captura
            if diff == 2:
                capturas.append(((linha_origem, coluna_origem),
                               (linha_destino, coluna_destino)))
            
            # Verificar se leva à promoção
            elif (self.jogador == Jogador.JOGADOR2 and linha_destino == 0):
                promocoes.append(((linha_origem, coluna_origem),
                                (linha_destino, coluna_destino)))
            
            # Verificar se é seguro
            elif self._eh_movimento_seguro(linha_destino, coluna_destino):
                movimentos_seguros.append(((linha_origem, coluna_origem),
                                         (linha_destino, coluna_destino)))
        
        # Priorizar: capturas > promoções > movimentos seguros > aleatório
        if capturas:
            # Preferir captura que leva a mais capturas
            return self._escolher_melhor_captura(capturas)
        
        if promocoes:
            return random.choice(promocoes)
        
        if movimentos_seguros:
            return random.choice(movimentos_seguros)
        
        return None
    
    def _escolher_melhor_captura(self, capturas: List) -> Tuple:
        """Escolhe a melhor captura, preferindo as que levam a mais capturas."""
        melhor = None
        max_sequencia = 0
        
        for movimento in capturas:
            (linha_origem, coluna_origem), (linha_destino, coluna_destino) = movimento
            
            # Simular movimento
            peca = self.jogo.tabuleiro.obter_peca(linha_origem, coluna_origem)
            if peca is None:
                continue

            peca_capturada = self.jogo.tabuleiro.obter_peca(
                (linha_origem + linha_destino) // 2,
                (coluna_origem + coluna_destino) // 2
            )
            tipo_original = peca.tipo
            
            try:
                # Fazer movimento temporário
                if peca_capturada:
                    self.jogo.tabuleiro.remover_peca(
                        (linha_origem + linha_destino) // 2,
                        (coluna_origem + coluna_destino) // 2
                    )
                if self.jogo.tabuleiro.mover_peca(
                    linha_origem, coluna_origem, linha_destino, coluna_destino
                ) is None:
                    continue

                self.jogo._promover_peca_se_necessario(peca)
                
                # Contar quantas capturas adicionais são possíveis
                proximas_capturas = self.jogo._encontrar_capturas(
                    linha_destino, coluna_destino
                )
                
                if len(proximas_capturas) > max_sequencia:
                    max_sequencia = len(proximas_capturas)
                    melhor = movimento
            finally:
                # Restaurar estado
                self.jogo.tabuleiro.mover_peca(
                    linha_destino, coluna_destino, linha_origem, coluna_origem
                )
                peca.tipo = tipo_original
                if peca_capturada:
                    self.jogo.tabuleiro.colocar_peca(
                        peca_capturada,
                        (linha_origem + linha_destino) // 2,
                        (coluna_origem + coluna_destino) // 2
                    )
        
        return melhor if melhor else random.choice(capturas)
    
    def _eh_movimento_seguro(self, linha: int, coluna: int) -> bool:
        """Verifica se uma posição de destino é segura."""
        # Uma posição é segura se não há peças inimigas adjacentes
        # que possam capturar a peça em movimento
        
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dir_linha, dir_coluna in direcoes:
            peca_adjacente_linha = linha + dir_linha
            peca_adjacente_coluna = coluna + dir_coluna
            
            if not self._posicao_valida(peca_adjacente_linha, peca_adjacente_coluna):
                continue
            
            peca_adjacente = self.jogo.tabuleiro.obter_peca(
                peca_adjacente_linha, peca_adjacente_coluna
            )
            
            if peca_adjacente and peca_adjacente.jogador != self.jogador:
                # Verificar se a peça inimiga pode capturar
                if self._pode_capturar(peca_adjacente_linha, peca_adjacente_coluna,
                                      linha, coluna):
                    return False
        
        return True
    
    def _pode_capturar(self, peca_linha: int, peca_coluna: int,
                      alvo_linha: int, alvo_coluna: int) -> bool:
        """Verifica se uma peça pode capturar na posição alvo."""
        peca = self.jogo.tabuleiro.obter_peca(peca_linha, peca_coluna)
        
        # Calcular direção
        dir_linha = 1 if alvo_linha > peca_linha else -1
        dir_coluna = 1 if alvo_coluna > peca_coluna else -1
        
        # Posição após captura
        pos_apos_linha = alvo_linha + dir_linha
        pos_apos_coluna = alvo_coluna + dir_coluna
        
        # Verificar se é movimento válido
        if not self._posicao_valida(pos_apos_linha, pos_apos_coluna):
            return False
        
        pos_apos = self.jogo.tabuleiro.obter_peca(pos_apos_linha, pos_apos_coluna)
        if pos_apos is not None:
            return False
        
        return True
    
    def _posicao_valida(self, linha: int, coluna: int) -> bool:
        """Verifica se uma posição está dentro do tabuleiro."""
        return (0 <= linha < Tabuleiro.TAMANHO and
                0 <= coluna < Tabuleiro.TAMANHO)
