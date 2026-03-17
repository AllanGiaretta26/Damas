"""
Módulo principal do jogo de damas.
Contém as classes Peca, Tabuleiro e Jogo que implementam a lógica do jogo.
"""

from enum import Enum
from typing import List, Tuple, Optional


class TipoPeca(Enum):
    """Enumeração para os tipos de peças."""
    PECA = 1
    DAMA = 2


class Jogador(Enum):
    """Enumeração para os jogadores."""
    JOGADOR1 = 1
    JOGADOR2 = 2


class Peca:
    """
    Representa uma peça do jogo de damas.
    
    Atributos:
        jogador: Qual jogador a peça pertence
        tipo: Se é uma peça comum ou dama
        linha: Linha da peça no tabuleiro (0-7)
        coluna: Coluna da peça no tabuleiro (0-7)
    """
    
    def __init__(self, jogador: Jogador, linha: int, coluna: int):
        """Inicializa uma peça."""
        self.jogador = jogador
        self.tipo = TipoPeca.PECA
        self.linha = linha
        self.coluna = coluna
    
    def promover(self):
        """Promove uma peça comum para dama."""
        self.tipo = TipoPeca.DAMA
    
    def mover(self, nova_linha: int, nova_coluna: int):
        """Move a peça para uma nova posição."""
        self.linha = nova_linha
        self.coluna = nova_coluna
    
    def eh_dama(self) -> bool:
        """Retorna True se a peça é uma dama."""
        return self.tipo == TipoPeca.DAMA
    
    def __repr__(self):
        tipo = "D" if self.eh_dama() else "P"
        jogador = "1" if self.jogador == Jogador.JOGADOR1 else "2"
        return f"{jogador}{tipo}"


class Tabuleiro:
    """
    Representa o tabuleiro do jogo de damas.
    
    O tabuleiro é 8x8 e apenas as casas pretas são usadas.
    As peças são colocadas nas primeiras 3 linhas para cada jogador.
    """
    
    TAMANHO = 8
    
    def __init__(self):
        """Inicializa o tabuleiro com as peças na posição inicial."""
        self.casas = [[None for _ in range(self.TAMANHO)] 
                      for _ in range(self.TAMANHO)]
        self._configurar_posicao_inicial()
    
    def _configurar_posicao_inicial(self):
        """Coloca as peças na posição inicial do jogo."""
        # Peças do Jogador 1 (linhas 0-2)
        for linha in range(3):
            for coluna in range(self.TAMANHO):
                if (linha + coluna) % 2 == 1:  # Apenas casas pretas
                    self.casas[linha][coluna] = Peca(Jogador.JOGADOR1, linha, coluna)
        
        # Peças do Jogador 2 (linhas 5-7)
        for linha in range(5, self.TAMANHO):
            for coluna in range(self.TAMANHO):
                if (linha + coluna) % 2 == 1:  # Apenas casas pretas
                    self.casas[linha][coluna] = Peca(Jogador.JOGADOR2, linha, coluna)
    
    def obter_peca(self, linha: int, coluna: int) -> Optional[Peca]:
        """Obtém a peça em uma posição específica."""
        if self._posicao_valida(linha, coluna):
            return self.casas[linha][coluna]
        return None
    
    def colocar_peca(self, peca: Peca, linha: int, coluna: int):
        """Coloca uma peça em uma posição."""
        if self._posicao_valida(linha, coluna):
            self.casas[linha][coluna] = peca
            peca.mover(linha, coluna)

    def mover_peca(self, linha_origem: int, coluna_origem: int,
                   linha_destino: int, coluna_destino: int) -> Optional[Peca]:
        """Move uma peça dentro do tabuleiro e retorna a peça movida."""
        if not (self._posicao_valida(linha_origem, coluna_origem) and
                self._posicao_valida(linha_destino, coluna_destino)):
            return None

        peca = self.obter_peca(linha_origem, coluna_origem)
        if peca is None or self.obter_peca(linha_destino, coluna_destino) is not None:
            return None

        self.casas[linha_origem][coluna_origem] = None
        self.casas[linha_destino][coluna_destino] = peca
        peca.mover(linha_destino, coluna_destino)
        return peca
    
    def remover_peca(self, linha: int, coluna: int) -> Optional[Peca]:
        """Remove e retorna uma peça."""
        if self._posicao_valida(linha, coluna):
            peca = self.casas[linha][coluna]
            self.casas[linha][coluna] = None
            return peca
        return None
    
    def _posicao_valida(self, linha: int, coluna: int) -> bool:
        """Verifica se uma posição está dentro do tabuleiro."""
        return 0 <= linha < self.TAMANHO and 0 <= coluna < self.TAMANHO
    
    def casa_preta(self, linha: int, coluna: int) -> bool:
        """Verifica se a casa é preta (onde as peças podem estar)."""
        return (linha + coluna) % 2 == 1
    
    def resetar(self):
        """Reseta o tabuleiro para a posição inicial."""
        self.casas = [[None for _ in range(self.TAMANHO)] 
                      for _ in range(self.TAMANHO)]
        self._configurar_posicao_inicial()


class Jogo:
    """
    Classe principal que gerencia a lógica do jogo de damas.
    
    Responsável por:
    - Gerenciar turnos
    - Validar movimentos
    - Detectar capturas e múltiplas capturas
    - Promover damas
    - Detectar fim de jogo
    """
    
    def __init__(self):
        """Inicializa um novo jogo."""
        self.tabuleiro = Tabuleiro()
        self.jogador_atual = Jogador.JOGADOR1
        self.peca_selecionada = None
        self.movimentos_validos = []
        self.historico_jogadas = []
        self.piezas_capturadas_j1 = 0
        self.piezas_capturadas_j2 = 0
        self.em_sequencia_captura = False
        self.linha_captura = None
        self.coluna_captura = None
    
    def selecionar_peca(self, linha: int, coluna: int) -> bool:
        """
        Seleciona uma peça para mover.
        
        Retorna True se a peça foi selecionada com sucesso.
        """
        peca = self.tabuleiro.obter_peca(linha, coluna)
        
        # Validar se a peça pertence ao jogador atual
        if peca is None or peca.jogador != self.jogador_atual:
            return False

        movimentos = self._calcular_movimentos_validos(linha, coluna)
        if not movimentos:
            return False

        self.peca_selecionada = peca
        self.movimentos_validos = movimentos
        return True
    
    def _calcular_movimentos_validos(self, linha: int, coluna: int) -> List[Tuple[int, int]]:
        """Calcula todos os movimentos válidos para uma peça."""
        peca = self.tabuleiro.obter_peca(linha, coluna)
        if peca is None or peca.jogador != self.jogador_atual:
            return []

        if self.em_sequencia_captura:
            if self.peca_selecionada is None:
                return []
            if (linha, coluna) != (self.peca_selecionada.linha, self.peca_selecionada.coluna):
                return []
            return self._encontrar_capturas(linha, coluna)

        capturas = self._encontrar_capturas(linha, coluna)
        if self._jogador_tem_capturas(self.jogador_atual):
            return capturas

        movimentos = []
        # Movimento simples
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dir_linha, dir_coluna in direcoes:
            nova_linha = linha + dir_linha
            nova_coluna = coluna + dir_coluna
            
            # Peças comuns só se movem para frente
            if peca.tipo == TipoPeca.PECA:
                if peca.jogador == Jogador.JOGADOR1 and dir_linha != 1:
                    continue
                if peca.jogador == Jogador.JOGADOR2 and dir_linha != -1:
                    continue
            
            # Verificar se o movimento é válido
            if self._movimento_simples_valido(nova_linha, nova_coluna):
                movimentos.append((nova_linha, nova_coluna))
        
        return movimentos
    
    def _movimento_simples_valido(self, linha: int, coluna: int) -> bool:
        """Verifica se um movimento simples é válido."""
        if not self._posicao_valida(linha, coluna):
            return False
        if not self.tabuleiro.casa_preta(linha, coluna):
            return False
        if self.tabuleiro.obter_peca(linha, coluna) is not None:
            return False
        return True
    
    def _encontrar_capturas(self, linha: int, coluna: int) -> List[Tuple[int, int]]:
        """Encontra todos os movimentos de captura válidos para uma peça."""
        peca = self.tabuleiro.obter_peca(linha, coluna)
        if peca is None:
            return []
        
        capturas = []
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dir_linha, dir_coluna in direcoes:
            nova_linha = linha + dir_linha * 2
            nova_coluna = coluna + dir_coluna * 2
            
            # Peças comuns só capturam para frente
            if peca.tipo == TipoPeca.PECA:
                if peca.jogador == Jogador.JOGADOR1 and dir_linha != 1:
                    continue
                if peca.jogador == Jogador.JOGADOR2 and dir_linha != -1:
                    continue
            
            # Verificar se a captura é válida
            peca_alvo = self.tabuleiro.obter_peca(
                linha + dir_linha, coluna + dir_coluna
            )
            
            if (self._movimento_simples_valido(nova_linha, nova_coluna) and
                peca_alvo is not None and
                peca_alvo.jogador != peca.jogador):
                capturas.append((nova_linha, nova_coluna))
        
        return capturas

    def _jogador_tem_capturas(self, jogador: Jogador) -> bool:
        """Verifica se o jogador possui alguma captura obrigatória no turno."""
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = self.tabuleiro.obter_peca(linha, coluna)
                if peca and peca.jogador == jogador:
                    if self._encontrar_capturas(linha, coluna):
                        return True
        return False
    
    def mover_peca(self, linha_origem: int, coluna_origem: int,
                   linha_destino: int, coluna_destino: int) -> bool:
        """
        Move uma peça de uma posição para outra.
        
        Retorna True se o movimento foi bem-sucedido.
        """
        peca = self.tabuleiro.obter_peca(linha_origem, coluna_origem)
        if peca is None or peca.jogador != self.jogador_atual:
            return False

        movimentos_validos = self._calcular_movimentos_validos(linha_origem, coluna_origem)

        # Validar movimento
        if (linha_destino, coluna_destino) not in movimentos_validos:
            return False

        self.peca_selecionada = peca
        self.movimentos_validos = movimentos_validos

        # Processar captura se houver
        diff_linha = abs(linha_destino - linha_origem)
        if diff_linha == 2:
            # É uma captura
            peca_capturada_linha = (linha_origem + linha_destino) // 2
            peca_capturada_coluna = (coluna_origem + coluna_destino) // 2
            peca_capturada = self.tabuleiro.remover_peca(
                peca_capturada_linha, peca_capturada_coluna
            )
            
            if peca_capturada:
                if peca_capturada.jogador == Jogador.JOGADOR1:
                    self.piezas_capturadas_j2 += 1
                else:
                    self.piezas_capturadas_j1 += 1
        else:
            peca_capturada = None

        if self.tabuleiro.mover_peca(linha_origem, coluna_origem, linha_destino, coluna_destino) is None:
            return False

        self._promover_peca_se_necessario(peca)
        # Registrar jogada
        self.historico_jogadas.append({
            'jogador': self.jogador_atual,
            'de': (linha_origem, coluna_origem),
            'para': (linha_destino, coluna_destino)
        })

        if diff_linha == 2:
            proximas_capturas = self._encontrar_capturas(linha_destino, coluna_destino)
            if proximas_capturas:
                self.em_sequencia_captura = True
                self.linha_captura = linha_destino
                self.coluna_captura = coluna_destino
                self.peca_selecionada = peca
                self.movimentos_validos = proximas_capturas
                return True

        self._encerrar_turno()
        return True
    
    def _tem_capturas_sequenciais_disponiveis(self) -> bool:
        """Verifica se há mais capturas disponíveis para a peça atual."""
        if self.peca_selecionada is None:
            return False
        capturas = self._encontrar_capturas(self.peca_selecionada.linha,
                                           self.peca_selecionada.coluna)
        return len(capturas) > 0
    
    def finalizar_movimento_captura(self) -> bool:
        """Finaliza um movimento de captura e passa para o próximo jogador."""
        if not self.em_sequencia_captura or self.movimentos_validos:
            return False

        self._encerrar_turno()
        return True

    def _promover_peca_se_necessario(self, peca: Peca):
        """Promove uma peça comum ao alcançar a última linha do oponente."""
        if peca.eh_dama():
            return

        if peca.jogador == Jogador.JOGADOR1 and peca.linha == 7:
            peca.promover()
        elif peca.jogador == Jogador.JOGADOR2 and peca.linha == 0:
            peca.promover()

    def _encerrar_turno(self):
        """Limpa o estado temporário do turno e passa a vez."""
        self.em_sequencia_captura = False
        self.linha_captura = None
        self.coluna_captura = None
        self.peca_selecionada = None
        self.movimentos_validos = []
        self._proxima_jogada()
    
    def _proxima_jogada(self):
        """Passa o turno para o próximo jogador."""
        self.jogador_atual = (Jogador.JOGADOR2 if 
                             self.jogador_atual == Jogador.JOGADOR1
                             else Jogador.JOGADOR1)
    
    def _posicao_valida(self, linha: int, coluna: int) -> bool:
        """Verifica se uma posição está dentro do tabuleiro."""
        return (0 <= linha < Tabuleiro.TAMANHO and
                0 <= coluna < Tabuleiro.TAMANHO)
    
    def verificar_fim_de_jogo(self) -> Tuple[bool, Optional[Jogador]]:
        """
        Verifica se o jogo acabou.
        
        Retorna (True, vencedor) se o jogo acabou, (False, None) caso contrário.
        """
        # Verificar se algum jogador não tem mais peças
        pecas_j1 = self._contar_pecas(Jogador.JOGADOR1)
        pecas_j2 = self._contar_pecas(Jogador.JOGADOR2)
        
        if pecas_j1 == 0:
            return (True, Jogador.JOGADOR2)
        if pecas_j2 == 0:
            return (True, Jogador.JOGADOR1)
        
        # Verificar se o jogador atual não tem movimentos disponíveis
        if not self._tem_movimentos_disponiveis(self.jogador_atual):
            outro_jogador = (Jogador.JOGADOR2 if
                           self.jogador_atual == Jogador.JOGADOR1
                           else Jogador.JOGADOR1)
            return (True, outro_jogador)
        
        return (False, None)
    
    def _contar_pecas(self, jogador: Jogador) -> int:
        """Conta quantas peças um jogador tem no tabuleiro."""
        count = 0
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = self.tabuleiro.obter_peca(linha, coluna)
                if peca and peca.jogador == jogador:
                    count += 1
        return count
    
    def _tem_movimentos_disponiveis(self, jogador: Jogador) -> bool:
        """Verifica se um jogador tem movimentos disponíveis."""
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = self.tabuleiro.obter_peca(linha, coluna)
                if peca and peca.jogador == jogador:
                    movimentos = self._calcular_movimentos_validos(linha, coluna)
                    if movimentos:
                        return True
        return False
    
    def resetar(self):
        """Reseta o jogo para o estado inicial."""
        self.tabuleiro.resetar()
        self.jogador_atual = Jogador.JOGADOR1
        self.peca_selecionada = None
        self.movimentos_validos = []
        self.historico_jogadas = []
        self.piezas_capturadas_j1 = 0
        self.piezas_capturadas_j2 = 0
        self.em_sequencia_captura = False
        self.linha_captura = None
        self.coluna_captura = None
