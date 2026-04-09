"""
Classe principal que gerencia a lógica do jogo de damas.
Refatorada para aplicar SOLID e Clean Code.
"""

from typing import List, Tuple, Optional
from src.models import Tabuleiro, Peca, Jogador
from src.services import MovimentoValidator, CaptureHandler, PromotionHandler


class Jogo:
    """
    Classe principal que gerencia a lógica do jogo de damas.
    
    Responsabilidades:
    - Gerenciar estado do jogo (turno, peças selecionadas)
    - Orquestrar serviços (validação, captura, promoção)
    - Manter histórico de jogadas
    - Detectar fim de jogo
    
    Segue SRP: orquestra serviços, não implementa regras diretamente.
    Segue DIP: depende de abstrações (serviços).
    """

    def __init__(self):
        """Inicializa um novo jogo."""
        self.tabuleiro = Tabuleiro()
        self.jogador_atual = Jogador.JOGADOR1
        
        # Estado de seleção
        self._peca_selecionada: Optional[Peca] = None
        self._movimentos_validos: List[Tuple[int, int]] = []
        
        # Histórico e estatísticas
        self.historico_jogadas: List[dict] = []
        self._pecas_capturadas_jogador1 = 0
        self._pecas_capturadas_jogador2 = 0
        
        # Estado de captura sequencial
        self._em_sequencia_captura = False
        
        # Inicializar serviços (Dependency Injection)
        self._movimento_validator = MovimentoValidator(self.tabuleiro)
        self._capture_handler = CaptureHandler(self.tabuleiro, self._movimento_validator)
        self._promotion_handler = PromotionHandler()

    @property
    def peca_selecionada(self) -> Optional[Peca]:
        """Obtém a peça selecionada."""
        return self._peca_selecionada

    @peca_selecionada.setter
    def peca_selecionada(self, peca: Optional[Peca]) -> None:
        """Define a peça selecionada."""
        self._peca_selecionada = peca

    @property
    def movimentos_validos(self) -> List[Tuple[int, int]]:
        """Obtém movimentos válidos para a peça selecionada."""
        return self._movimentos_validos

    @movimentos_validos.setter
    def movimentos_validos(self, movimentos: List[Tuple[int, int]]) -> None:
        """Define movimentos válidos."""
        self._movimentos_validos = movimentos

    @property
    def em_sequencia_captura(self) -> bool:
        """Verifica se está em sequência de captura."""
        return self._em_sequencia_captura

    @em_sequencia_captura.setter
    def em_sequencia_captura(self, valor: bool) -> None:
        """Define estado de sequência de captura."""
        self._em_sequencia_captura = valor

    @property
    def piezas_capturadas_j1(self) -> int:
        """Retorna peças capturadas pelo jogador 1."""
        return self._pecas_capturadas_jogador1

    @piezas_capturadas_j1.setter
    def piezas_capturadas_j1(self, valor: int) -> None:
        """Define peças capturadas pelo jogador 1."""
        self._pecas_capturadas_jogador1 = valor

    @property
    def piezas_capturadas_j2(self) -> int:
        """Retorna peças capturadas pelo jogador 2."""
        return self._pecas_capturadas_jogador2

    @piezas_capturadas_j2.setter
    def piezas_capturadas_j2(self, valor: int) -> None:
        """Define peças capturadas pelo jogador 2."""
        self._pecas_capturadas_jogador2 = valor

    def selecionar_peca(self, linha: int, coluna: int) -> bool:
        """
        Seleciona uma peça para mover.
        
        Args:
            linha: Linha da peça
            coluna: Coluna da peça
            
        Returns:
            True se a peça foi selecionada com sucesso
        """
        peca = self.tabuleiro.obter_peca(linha, coluna)

        # Validar se a peça pertence ao jogador atual
        if peca is None or not peca.pertence_ao_jogador(self.jogador_atual):
            return False

        movimentos = self._movimento_validator.calcular_movimentos_validos(
            linha, coluna, self.jogador_atual, 
            self._em_sequencia_captura, self._peca_selecionada
        )
        
        if not movimentos:
            return False

        self._peca_selecionada = peca
        self._movimentos_validos = movimentos
        return True

    def mover_peca(self, linha_origem: int, coluna_origem: int,
                   linha_destino: int, coluna_destino: int) -> bool:
        """
        Move uma peça de uma posição para outra.
        
        Args:
            linha_origem: Linha de origem
            coluna_origem: Coluna de origem
            linha_destino: Linha de destino
            coluna_destino: Coluna de destino
            
        Returns:
            True se o movimento foi bem-sucedido
        """
        peca = self.tabuleiro.obter_peca(linha_origem, coluna_origem)
        if peca is None or not peca.pertence_ao_jogador(self.jogador_atual):
            return False

        movimentos_validos = self._movimento_validator.calcular_movimentos_validos(
            linha_origem, coluna_origem, self.jogador_atual,
            self._em_sequencia_captura, self._peca_selecionada
        )

        # Validar movimento
        if (linha_destino, coluna_destino) not in movimentos_validos:
            return False

        self._peca_selecionada = peca
        self._movimentos_validos = movimentos_validos

        # Verificar se é captura
        diff_linha = abs(linha_destino - linha_origem)
        eh_captura = diff_linha == 2
        
        if eh_captura:
            peca_capturada = self._capture_handler.executar_captura(
                linha_origem, coluna_origem, linha_destino, coluna_destino
            )
            
            if peca_capturada:
                self._registrar_captura(peca_capturada)
        else:
            # Movimento simples
            if self.tabuleiro.mover_peca(
                linha_origem, coluna_origem, linha_destino, coluna_destino
            ) is None:
                return False

        # Tentar promoção
        self._promotion_handler.tentar_promover(peca)
        
        # Registrar jogada
        self._registrar_jogada(linha_origem, coluna_origem, 
                              linha_destino, coluna_destino)

        # Verificar capturas sequenciais
        if eh_captura:
            if self._capture_handler.tem_capturas_sequenciais(linha_destino, coluna_destino):
                self._em_sequencia_captura = True
                self._peca_selecionada = peca
                self._movimentos_validos = self._capture_handler.obter_capturas_sequenciais(
                    linha_destino, coluna_destino
                )
                return True

        # Encerrar turno
        self._encerrar_turno()
        return True

    def _registrar_captura(self, peca_capturada: Peca) -> None:
        """Registra uma captura para estatísticas."""
        if peca_capturada.pertence_ao_jogador(Jogador.JOGADOR1):
            self._pecas_capturadas_jogador2 += 1
        else:
            self._pecas_capturadas_jogador1 += 1

    def _registrar_jogada(self, linha_origem: int, coluna_origem: int,
                         linha_destino: int, coluna_destino: int) -> None:
        """Registra uma jogada no histórico."""
        self.historico_jogadas.append({
            'jogador': self.jogador_atual,
            'de': (linha_origem, coluna_origem),
            'para': (linha_destino, coluna_destino)
        })

    def _encerrar_turno(self) -> None:
        """Limpa o estado temporário do turno e passa a vez."""
        self._em_sequencia_captura = False
        self._peca_selecionada = None
        self._movimentos_validos = []
        self._alternar_jogador()

    def _alternar_jogador(self) -> None:
        """Passa o turno para o próximo jogador."""
        self.jogador_atual = (Jogador.JOGADOR2 
                             if self.jogador_atual == Jogador.JOGADOR1 
                             else Jogador.JOGADOR1)

    def verificar_fim_de_jogo(self) -> Tuple[bool, Optional[Jogador]]:
        """
        Verifica se o jogo acabou.
        
        Returns:
            (True, vencedor) se o jogo acabou, (False, None) caso contrário.
        """
        # Verificar se algum jogador não tem mais peças
        pecas_j1 = self.tabuleiro.contar_pecas(Jogador.JOGADOR1)
        pecas_j2 = self.tabuleiro.contar_pecas(Jogador.JOGADOR2)

        if pecas_j1 == 0:
            return (True, Jogador.JOGADOR2)
        if pecas_j2 == 0:
            return (True, Jogador.JOGADOR1)

        # Verificar se o jogador atual não tem movimentos disponíveis
        if not self._movimento_validator.tem_movimentos_disponiveis(self.jogador_atual):
            outro_jogador = (Jogador.JOGADOR2 
                           if self.jogador_atual == Jogador.JOGADOR1 
                           else Jogador.JOGADOR1)
            return (True, outro_jogador)

        return (False, None)

    def resetar(self) -> None:
        """Reseta o jogo para o estado inicial."""
        self.tabuleiro.resetar()
        self.jogador_atual = Jogador.JOGADOR1
        self._peca_selecionada = None
        self._movimentos_validos = []
        self.historico_jogadas = []
        self._pecas_capturadas_jogador1 = 0
        self._pecas_capturadas_jogador2 = 0
        self._em_sequencia_captura = False

    # Métodos públicos para acesso aos serviços (para IA e testes)
    def obter_movimentos_validos_para_peca(self, linha: int, coluna: int) -> List[Tuple[int, int]]:
        """Obtém movimentos válidos para uma peça (usado pela IA e testes)."""
        return self._movimento_validator.calcular_movimentos_validos(
            linha, coluna, self.jogador_atual
        )

    def jogador_tem_capturas(self, jogador: Jogador) -> bool:
        """Verifica se um jogador tem capturas disponíveis (usado pela IA)."""
        return self._movimento_validator._jogador_tem_capturas(jogador)

    def encontrar_capturas_para_peca(self, linha: int, coluna: int) -> List[Tuple[int, int]]:
        """Encontra capturas para uma peça (usado pela IA)."""
        return self._movimento_validator.encontrar_capturas(linha, coluna)

    def tentar_promover_peca(self, peca: Peca) -> bool:
        """Tenta promover uma peça (usado pela IA para simulação)."""
        return self._promotion_handler.tentar_promover(peca)
