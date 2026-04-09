"""
Serviço de promoção de peças no jogo de damas.
Responsável por aplicar o Single Responsibility Principle (SRP).
"""

from src.models.peca import Peca
from src.models.enums import Jogador


class PromotionHandler:
    """
    Gerencia promoção de peças no jogo de damas.
    
    Responsabilidades:
    - Verificar se uma peça deve ser promovida
    - Executar a promoção
    
    Segue SRP: apenas gerencia promoções.
    """

    @staticmethod
    def tentar_promover(peca: Peca) -> bool:
        """
        Tenta promover uma peça se ela atingiu a última linha.
        
        Jogador 1 (Vermelho): promove ao alcançar linha 0 (topo)
        Jogador 2 (Azul): promove ao alcançar linha 7 (base)
        
        Args:
            peca: Peça a ser promovida
            
        Returns:
            True se a peça foi promovida, False caso contrário
        """
        if peca.eh_dama():
            return False

        # J1 promove na linha 0 (topo), J2 promove na linha 7 (base)
        if peca.pertence_ao_jogador(Jogador.JOGADOR1) and peca.linha == 0:
            peca.promover()
            return True
        elif peca.pertence_ao_jogador(Jogador.JOGADOR2) and peca.linha == 7:
            peca.promover()
            return True
        
        return False
