"""
Serviço de gerenciamento de capturas no jogo de damas.
Responsável por aplicar o Single Responsibility Principle (SRP).
"""

from typing import List, Tuple, Optional
from src.models.tabuleiro import Tabuleiro
from src.models.peca import Peca
from src.models.enums import Jogador
from src.services.movimento_validator import MovimentoValidator


class CaptureHandler:
    """
    Gerencia lógica de capturas no jogo de damas.
    
    Responsabilidades:
    - Executar capturas
    - Verificar capturas sequenciais
    - Contabilizar peças capturadas
    
    Segue SRP: apenas gerencia capturas, não outras regras.
    """

    def __init__(self, tabuleiro: Tabuleiro, validator: MovimentoValidator):
        """Inicializa o handler com tabuleiro e validador."""
        self._tabuleiro = tabuleiro
        self._validator = validator

    def executar_captura(self, linha_origem: int, coluna_origem: int,
                        linha_destino: int, coluna_destino: int) -> Optional[Peca]:
        """
        Executa uma captura e retorna a peça capturada.
        
        Args:
            linha_origem: Linha de origem da peça que captura
            coluna_origem: Coluna de origem da peça que captura
            linha_destino: Linha de destino da peça que captura
            coluna_destino: Coluna de destino da peça que captura
            
        Returns:
            A peça capturada ou None se falhar
        """
        peca_capturada_linha = (linha_origem + linha_destino) // 2
        peca_capturada_coluna = (coluna_origem + coluna_destino) // 2
        
        peca_capturada = self._tabuleiro.remover_peca(
            peca_capturada_linha, peca_capturada_coluna
        )

        if peca_capturada:
            self._tabuleiro.mover_peca(
                linha_origem, coluna_origem, linha_destino, coluna_destino
            )

        return peca_capturada

    def tem_capturas_sequenciais(self, linha: int, coluna: int) -> bool:
        """
        Verifica se há capturas sequenciais disponíveis a partir de uma posição.
        
        Args:
            linha: Linha da peça
            coluna: Coluna da peça
            
        Returns:
            True se há capturas sequenciais disponíveis
        """
        capturas = self._validator.encontrar_capturas(linha, coluna)
        return len(capturas) > 0

    def obter_capturas_sequenciais(self, linha: int, coluna: int) -> List[Tuple[int, int]]:
        """
        Obtém capturas sequenciais disponíveis.
        
        Args:
            linha: Linha da peça
            coluna: Coluna da peça
            
        Returns:
            Lista de tuplas (linha, coluna) para capturas sequenciais
        """
        return self._validator.encontrar_capturas(linha, coluna)
